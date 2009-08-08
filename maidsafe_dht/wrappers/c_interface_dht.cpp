#include <stdio.h>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include <boost/cstdint.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/progress.hpp>
#include <cryptopp/integer.h>
#include <cryptopp/osrng.h>

#include <exception>
#include <vector>
#include <list>
#include <set>

#include "base/crypto.h"
#include "base/rsakeypair.h"
#include "kademlia/kadutils.h"
#include "kademlia/knodeimpl.h"
#include "maidsafe/maidsafe-dht.h"
#include "tests/kademlia/fake_callbacks.h"
#include "transport/transportapi.h"

#include "c_interface_dht.h"
#include<fstream>

namespace fs = boost::filesystem;
const int kNetworkSize = 5;
const int kTestK = 4;


void initialise_and_connect_to_network(char* , int, int );
void disconnect_from_network();

std::string kad_config_file_("");
std::vector< boost::shared_ptr<rpcprotocol::ChannelManager> >
    channel_managers_;
std::vector< boost::shared_ptr<kad::KNode> > knodes_;
std::vector<std::string> dbs_;
crypto::Crypto cry_obj_;
GeneralKadCallback cb_;
std::vector<std::string> node_ids_;
std::set<boost::uint16_t> ports_;
std::string test_dir_;

std::string ar_ip_addr="";

int ar_ip_port=0;
int port_to_start=0;// port on which to start


int IF_CONNECTED=0;

//std::ofstream fout("/tmp/log",std::ios::out);

inline void create_rsakeys(std::string *pub_key, std::string *priv_key) 
{
   crypto::RsaKeyPair kp;
   kp.GenerateKeys(512);
   *pub_key =  kp.public_key();
   *priv_key = kp.private_key();
}

inline void create_req(const std::string &pub_key, const std::string &priv_key,
    const std::string &key, std::string *sig_pub_key, std::string *sig_req) 
{
   crypto::Crypto cobj;
   cobj.set_symm_algorithm("AES_256");
   cobj.set_hash_algorithm("SHA512");
   *sig_pub_key = cobj.AsymSign(pub_key, "", priv_key, crypto::STRING_STRING);
   *sig_req = cobj.AsymSign(cobj.Hash(pub_key + *sig_pub_key + key, "",
   crypto::STRING_STRING, true), "", priv_key, crypto::STRING_STRING);
}


std::string get_app_directory() {
  boost::filesystem::path app_path;
#if defined(MAIDSAFE_POSIX)
  app_path = boost::filesystem::path("/var/cache/maidsafe/",
      boost::filesystem::native);
#elif defined(MAIDSAFE_WIN32)
  TCHAR szpth[MAX_PATH];
  if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_COMMON_APPDATA, NULL, 0, szpth))) {
    std::ostringstream stm;
    const std::ctype<char> &ctfacet =
        std::use_facet< std::ctype<char> >(stm.getloc());
    for (size_t i = 0; i < wcslen(szpth); ++i)
      stm << ctfacet.narrow(szpth[i], 0);
    app_path = boost::filesystem::path(stm.str(),
                                       boost::filesystem::native);
    app_path /= "maidsafe";
  }
#elif defined(MAIDSAFE_APPLE)
  app_path = boost::filesystem::path("/Library/maidsafe/", fs::native);
#endif
  return app_path.string();
}


void wrapper_for_dht_start_as_server(int port)
{


    test_dir_ = std::string("KnodeTest") +
                boost::lexical_cast<std::string>(base::random_32bit_uinteger());
    kad_config_file_ = test_dir_ + std::string("/.kadconfig");

      if (fs::exists(test_dir_))
        fs::remove_all(test_dir_);
      fs::create_directories(test_dir_);
    // setup the nodes without starting them
    for (int  i = 0; i < 9; ++i) {
      boost::shared_ptr<rpcprotocol::ChannelManager>
          channel_manager_local_(new rpcprotocol::ChannelManager());
      channel_managers_.push_back(channel_manager_local_);

      std::string db_local_ = test_dir_ + std::string("/datastore") +
                              base::itos(i);
      dbs_.push_back(db_local_);

      boost::shared_ptr<kad::KNode>
          knode_local_(new kad::KNode(dbs_[i],
                                      channel_managers_[i],
                                      kad::VAULT,
                                      kTestK,
                                      kad::kAlpha,
                                      kad::kBeta));
      channel_managers_[i]->StartTransport(port+i,
          boost::bind(&kad::KNode::HandleDeadRendezvousServer,
          knode_local_.get(), _1));
      knodes_.push_back(knode_local_);
      ports_.insert(knodes_[i]->host_port());
//	std::cout<<" Debug::port for "<<i<<" is "<<knodes_[i]->host_port()<<std::endl;
      cb_.Reset();
    }

    // start node 1 and add his details to kad config protobuf
    kad_config_file_ = dbs_[1] + "/.kadconfig";
    knodes_[1]->Join("",
                     kad_config_file_,
                     boost::bind(&GeneralKadCallback::CallbackFunc, &cb_, _1),
                     false);
    wait_result(&cb_);
    if( kad::kRpcResultSuccess !=  cb_.result())
	{
		std::cout<<" Server could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
    if( !knodes_[1]->is_joined())
	{
		std::cout<<" Server could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
    printf("Node 1 joined.\n");
    base::KadConfig kad_config;
    base::KadConfig::Contact *kad_contact_ = kad_config.add_contact();
    std::string hex_id("");
    base::encode_to_hex(knodes_[1]->node_id(), &hex_id);
    kad_contact_->set_node_id(hex_id);
    
	kad_contact_->set_ip(knodes_[1]->host_ip());
	std::string s="192.168.1.2";
        //kad_contact_->set_ip(s);
    kad_contact_->set_port(knodes_[1]->host_port());
    //kad_contact_->set_port(44693);
    //kad_contact_->set_port(9570);
   // kad_contact_->set_port(27436);
    kad_contact_->set_local_ip(knodes_[1]->local_host_ip());
    kad_contact_->set_local_port(knodes_[1]->local_host_port());
    std::string node1_id = knodes_[1]->node_id();
    kad_config_file_ = dbs_[0] + "/.kadconfig";
    std::fstream output1(kad_config_file_.c_str(),
      std::ios::out | std::ios::trunc | std::ios::binary);
    kad_config.SerializeToOstream(&output1);
    output1.close();
	char cat_cmd[150];
	sprintf( cat_cmd, "cat %s", kad_config_file_.c_str() );
	system( cat_cmd );

	 


    // bootstrap node 0 (off node 1) and reset kad config with his details
    cb_.Reset();
    knodes_[0]->Join("",
                     kad_config_file_,
                     boost::bind(&GeneralKadCallback::CallbackFunc, &cb_, _1),
                     false);
    wait_result(&cb_);
    if( kad::kRpcResultSuccess !=  cb_.result())
	{
		std::cout<<" Node could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
    if( !knodes_[0]->is_joined())
	{
		std::cout<<" Node could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
    printf("Node 0 joined.\n");
    node_ids_.push_back(knodes_[0]->node_id());
    kad_config.Clear();
    kad_contact_ = kad_config.add_contact();
    std::string hex_id1("");
    base::encode_to_hex(knodes_[0]->node_id(), &hex_id1);
    kad_contact_->set_node_id(hex_id1);
    kad_contact_->set_ip(knodes_[0]->host_ip());
    kad_contact_->set_port(knodes_[0]->host_port());
    kad_contact_->set_local_ip(knodes_[0]->local_host_ip());
    kad_contact_->set_local_port(knodes_[0]->local_host_port());

    for (int i = 1; i < kNetworkSize; i++) {
      kad_config_file_ = dbs_[i] + "/.kadconfig";
      std::fstream output2(kad_config_file_.c_str(),
        std::ios::out | std::ios::trunc | std::ios::binary);
      kad_config.SerializeToOstream(&output2);
      output2.close();
    }



    // start the rest of the nodes (including node 1 again)
    for (int  i = 2; i < 9; ++i) {
      std::string id("");
      if (i == 1) {
        id = node1_id;
      }
      cb_.Reset();
      kad_config_file_ = dbs_[i] + "/.kadconfig";
      knodes_[i]->Join(id,
                       kad_config_file_,
                       boost::bind(&GeneralKadCallback::CallbackFunc, &cb_, _1),
                       false);
      wait_result(&cb_);
    if( kad::kRpcResultSuccess !=  cb_.result())
	{
		std::cout<<" Node could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
    if( !knodes_[i]->is_joined())
	{
		std::cout<<" Node could not be started .. "<<std::endl;
		std::cout<<" Exiting .. "<<std::endl;
		return;
	}
      printf("Node %i joined.\n", i);
      node_ids_.push_back(knodes_[i]->node_id());
    }
    cb_.Reset();
    printf("*-----------------------------------*\n");
    printf("*  9 local Kademlia nodes running  *\n");
    printf("*-----------------------------------*\n\n");

	char ch='n';
	
   while(ch!='y')
   {
   sleep(2);
	std::cout<<" Enter \'y\' to disconnect from network"<<std::endl;
	std::cin>>ch;
   }

	std::cout<<" disconnecting from the network ..... "<<std::endl;
	for (int i = 8; i >= 1; i--) {
      knodes_[i]->StopRvPing();
    }
    for (int i = 8; i >= 0; i--) {
      printf("stopping node %i\n", i);
      cb_.Reset();
      knodes_[i]->Leave();
      //EXPECT_FALSE(knodes_[i]->is_joined());
      channel_managers_[i]->StopTransport();
      knodes_[i].reset();
      channel_managers_[i].reset();
    }
    std::set<boost::uint16_t>::iterator it;
    for (it = ports_.begin(); it != ports_.end(); it++) 
	{
      // Deleting the DBs in the app dir
        	fs::path db_dir(get_app_directory());
      		db_dir /= base::itos(*it);
                if (fs::exists(db_dir))
                      fs::remove_all(db_dir);
	}
	if (fs::exists(test_dir_))
        fs::remove_all(test_dir_);


	 knodes_.clear();
    channel_managers_.clear();
    dbs_.clear();
    node_ids_.clear();
    ports_.clear();
    std::cout<<"Disconnected from the network......."<<std::cout;

      
	


}

void initialise_and_connect_to_network(char* ip, int pport, int pport_to_start)
{

if ( IF_CONNECTED == 1 )
{
//fout<<"coming out "<<std::endl;
return ;
}

     std::string ip_addr=ip;
  //   std::cout<<" Connecting to the network ...  "<<std::endl;
     test_dir_ = std::string("KnodeTest") +
     boost::lexical_cast<std::string>(base::random_32bit_uinteger());
     kad_config_file_ = test_dir_ + std::string("/.kadconfig");

     if (fs::exists(test_dir_))
        fs::remove_all(test_dir_);
     
     fs::create_directories(test_dir_);



      boost::shared_ptr<rpcprotocol::ChannelManager>
      channel_manager_local_(new rpcprotocol::ChannelManager());
      std::string db_local_ = test_dir_ + std::string("/datastore") +
                              base::itos(0);

      channel_managers_.push_back(channel_manager_local_);

      boost::shared_ptr<kad::KNode>
      knode_local_(new kad::KNode(db_local_,
                                      channel_managers_[0],
                                      kad::VAULT,
                                      kTestK,
                                 kad::kAlpha,
                                      kad::kBeta));


	
       channel_managers_[0]->StartTransport(pport_to_start,
          boost::bind(&kad::KNode::HandleDeadRendezvousServer,
          knode_local_.get(), _1));
      
      knodes_.push_back(knode_local_);

      ports_.insert(knodes_[0]->host_port());
      cb_.Reset();


    kad_config_file_ = db_local_ + "/.kadconfig";
    base::KadConfig kad_config;
    base::KadConfig::Contact *kad_contact_ = kad_config.add_contact();
    std::string hex_id("");
    base::encode_to_hex(knodes_[0]->node_id(), &hex_id);
    kad_contact_->set_node_id(hex_id);
    kad_contact_->set_ip(knodes_[0]->host_ip());
    std::string s=ar_ip_addr;
    kad_contact_->set_ip(ip_addr);
    //kad_contact_->set_port(knodes_[0]->host_port());
    kad_contact_->set_port(pport);
    kad_contact_->set_local_ip(knodes_[0]->local_host_ip());

    kad_contact_->set_local_port(knodes_[0]->local_host_port());
    std::string node1_id = knodes_[0]->node_id();
    kad_config_file_ = db_local_ + "/.kadconfig";
    std::fstream output1(kad_config_file_.c_str(),
    std::ios::out | std::ios::trunc | std::ios::binary);
    kad_config.SerializeToOstream(&output1);
    output1.close();

    cb_.Reset();
    knodes_[0]->Join("",
                     kad_config_file_,
                     boost::bind(&GeneralKadCallback::CallbackFunc, &cb_, _1),
                     false);


     wait_result(&cb_);
	IF_CONNECTED=1;


}
void wrapper_for_dht_put(char *key1 , char *value1)
{

     int i;
     std::string value = value1;
     std::string key = key1; 
    
     StoreValueCallback cb_;
     std::string pub_key, priv_key, sig_pub_key, sig_req;
     create_rsakeys(&pub_key, &priv_key);
     create_req(pub_key, priv_key, key, &sig_pub_key, &sig_req);

     boost::int32_t before_store = base::get_epoch_milliseconds();

     knodes_[0]->StoreValue(key, value, pub_key, sig_pub_key, sig_req,
                             boost::bind(&StoreValueCallback::CallbackFunc, &cb_, _1));

     wait_result(&cb_);

     
    if ( kad::kRpcResultSuccess ==  cb_.result() )
                std::cout<<" Store was sucessful "<<std::endl;
     else
                std::cout<<" Store failed "<<std::endl;
	

}


std::string findValue;	
char const  * wrapper_for_dht_get(char *key1 ,int flag)
{
	bool got_value=false;
	std::string key = key1;
	FindCallback cb_1;
	cb_1.Reset();
	findValue="";	
       
        knodes_[0]->FindValue(key,
        boost::bind(&FindCallback::CallbackFunc, &cb_1, _1));
        wait_result(&cb_1);

       if ( kad::kRpcResultSuccess == cb_1.result())
       {
	        std::cout<<" Search operation was successful "<<std::endl;
        }
       else
        {
        	std::cout<<" Search operaton failed "<<std::endl;
        }
  
        int tempi=cb_1.values().size()-1;
        unsigned int i=(flag)?0: ( tempi<0?0:tempi);
     
//        std::cout<<i<<" tempi " <<tempi;

	for (i ; i < cb_1.values().size(); i++) 
	{

   		        std::cout << cb_1.values()[i] << std::endl;
			std::string temp=cb_1.values()[i];
			//strcpy(value1,temp.c_str());
			if(flag)
			    findValue=  i?(findValue+"|"+ temp):"|"+temp ;
			else
			    findValue=temp;
	}
       	  cb_1.Reset();
    
    
    return findValue.c_str();
}

void disconnect_from_network()
{
      boost::this_thread::sleep(boost::posix_time::seconds(5));
      knodes_[0]->StopRvPing();
      cb_.Reset();
      knodes_[0]->Leave();
      channel_managers_[0]->StopTransport();
      knodes_[0].reset();
      channel_managers_[0].reset();


}
/*
int main(int argc, char **argv)
{
	ar_ip_addr=argv[1];
	std::string temp=argv[2];
	ar_ip_port=atoi(temp.c_str());
	std::cout<<" inside main "<<std::endl;
	std::cout<<" value of ip addr is "<<ar_ip_addr<<std::endl;
	
	char *key=new char(10);
	char *value=new char(10);
	int i;
	for(i=0;i<10;i++)
		value[i]='0';
	strcpy(key,"arif");
//	strcpy(value,"reddy");
	wrapper_for_dht_get(argv[1], ar_ip_port , key , value );
	
	return 0;

}

*/
