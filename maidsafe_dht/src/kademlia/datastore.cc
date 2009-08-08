/* Copyright (c) 2009 maidsafe.net limited
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
    * Neither the name of the maidsafe.net limited nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include "kademlia/datastore.h"

#include <exception>
#include "base/config.h"
#include "maidsafe/maidsafe-dht.h"
#include "kademlia/EncapsulatedObject.pb.h"


static std::string convert_to_string(void *to_convert , int size )
{

        std::string to_return((const char*)to_convert, (size_t) size );
	free(to_convert);
	return to_return;

}

class temp_store_time{
public:
boost::uint32_t last_published_time;
boost::uint32_t original_published_time;
};

namespace kad {

DataStore::DataStore():db_(), is_open_(false) 
{

}

DataStore::~DataStore() 
{
	if (is_open_)
    		Close();
}

bool DataStore::Init(const std::string &file_name,
    bool reuse_database) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::Init "<<std::endl;
#endif 
	int ecode;	


	if ( (db_ = tcbdbnew()) == NULL )
	{
		fprintf(stderr, "tcbdbnew() error: \n");
		return false;
	}
	if (!boost::filesystem::exists(file_name)) 
	{
      		// create a new one
		if(!tcbdbopen(db_, file_name.c_str(), BDBOWRITER | BDBOCREAT))
		{
  			ecode = tcbdbecode(db_);
    			fprintf(stderr, "open error: %s\n", tcbdberrmsg(ecode));
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Init "<<std::endl;
#endif 
			return false;
  		}
	}
	else
	{
		if (!reuse_database) 
		{
			if(!tcbdbopen(db_, file_name.c_str(), BDBOWRITER | BDBOTRUNC))
                	{
                       		 ecode = tcbdbecode(db_);
                    		 fprintf(stderr, "open error: %s\n", tcbdberrmsg(ecode));

#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Init "<<std::endl;
#endif 
				 return false;
                	}

			
		}
		else
		{
			if(!tcbdbopen(db_, file_name.c_str(), BDBOWRITER | BDBOCREAT))
                	{
                       		 ecode = tcbdbecode(db_);
                       		 fprintf(stderr, "open error: %s\n", tcbdberrmsg(ecode));
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Init "<<std::endl;
#endif 
				return false;
                	}
		}

	}
	is_open_=true;
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Init "<<std::endl;
#endif 
	return true;


}

bool DataStore::Close() 
{

#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::Close "<<std::endl;
#endif 
	bool result=false;
	if ( result =  tcbdbclose(db_) )
		is_open_= false;
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Close "<<std::endl;
#endif 
  	return result;
}

bool DataStore::Keys(std::vector<std::string> *keys) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::Keys "<<std::endl;
#endif 
	keys->clear();
	int ecode;
	BDBCUR *cur;
	if ( !(cur = tcbdbcurnew(db_)) )
	{
		ecode = tcbdbecode(db_);
                fprintf(stderr, "open error: %s\n", tcbdberrmsg(ecode));
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Keys "<<std::endl;
#endif
                return false;

	}		
	if ( !tcbdbcurfirst(cur)) 
	{
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Keys "<<std::endl;
#endif	
		//tcbdbcurdel(cur);
                return true;

	}
	void * keyval;
	void * retval;
	int sp=0;
	while((retval = tcbdbcurkey(cur,&sp)) != NULL)
	{
		std::string to_store= ::convert_to_string( retval , sp );
		keys->push_back(to_store);	
		 tcbdbcurnext(cur);
		
	}
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::Keys "<<std::endl;
#endif
	if(cur)
	tcbdbcurdel(cur); 
	return true;

}

inline bool DataStore::KeyValueExists(const std::string &key,
    const std::string &value) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::KeyValueExists "<<std::endl;
#endif 
	bool result = false;
	void *kbuf=(void*)key.c_str();
	int ksiz=key.length();
	TCLIST *L = tcbdbget4(db_, kbuf, ksiz);
	if(L==NULL)
	{
		result=false;
	}
	else
	{
		void *val;
		void *retval;
		int sp=0;
		while( !result && (retval=tclistpop( L, &sp )) )
		{
                	std::string to_parse= ::convert_to_string( retval , sp );
			EncapsulatedObject obj;
			if( ! obj.ParseFromString(to_parse) )
			{
				// cleanup and go out
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::KeyValueExists "<<std::endl;
#endif
				return false;

			}
			std::string to_test=obj.data();
			if( to_test == value )
			{
				result=true;
			}

		}
	}
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::KeyValueExists "<<std::endl;
#endif 
	if(result)
	tclistdel( L ) ;
  	return result;
}

inline bool DataStore::KeyExists(const std::string &key)
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::KeyExists "<<std::endl;
#endif 
        bool result = false;
        void *kbuf=(void*)key.c_str();
        int ksiz=key.length();
	int sp;
        void *retval = tcbdbget(db_, kbuf, ksiz , &sp );
        if(retval != NULL)
        {
		free(retval);
                result=true;
        }
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::KeyExists "<<std::endl;
#endif 
        return result;

}

bool DataStore::StoreItem(const std::string &key,
    const std::string &value,
    boost::uint32_t last_published_time,
    boost::uint32_t original_published_time) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::StoreItem "<<std::endl;
#endif 
	if ((key.size() == 0) || (value.size() == 0) || (last_published_time <= 0) || (original_published_time <= 0)) 
	{
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::StoreItem "<<std::endl;
#endif 
    		return false;
	}

	bool result=false;
	
	if( KeyValueExists(key,value)  )	
	{
		if( ! DeleteItem(key,value) )	
		{
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::StoreItem "<<std::endl;
#endif 
			return false;
		}
	}
	std::string to_store;
	EncapsulatedObject obj;
	obj.set_data(value);
	obj.set_last_published_time(last_published_time);
	obj.set_original_published_time(original_published_time);
       	if ( !obj.SerializeToString(&to_store) )
	{
		// cleanup and go out
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::StoreItem "<<std::endl;
#endif
                return false;

	}
	void *keyval=(void * ) key.c_str();
	int keyval_length=key.length();
	void *val=(void *) to_store.c_str();
	size_t len=to_store.length();
	
	if (  tcbdbputdup(db_, keyval , keyval_length , val , len ) )
	{
		result=true;	
	}
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::StoreItem "<<std::endl;
#endif 
	return result;
}

bool DataStore::LoadItem(const std::string &key,
    std::vector<std::string> &values) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::LoadItem "<<std::endl;
#endif 
        bool result = false;
        void *kbuf=(void*)key.c_str();
        int ksiz=key.length();
        TCLIST *L = tcbdbget4(db_, kbuf,  ksiz);
        if(L==NULL)
        {
                result=false;
        }
        else
        {
                void *val;
                void *retval;
                int sp=0;
                while( (retval=tclistpop( L, &sp )) )
                {
                        std::string to_parse=::convert_to_string(retval,sp);
                        EncapsulatedObject obj;
                        obj.ParseFromString(to_parse);
                        std::string to_store=obj.data();
			values.push_back(to_store);

                }
		result = true ;
        }
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::LoadItem "<<std::endl;
#endif 
	if(result)
	tclistdel( L ) ;
        return result;

}

bool DataStore::DeleteKey(const std::string &key) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::DeleteKey "<<std::endl;
#endif 
	bool result = false;
        void *kbuf=(void*)key.c_str();
        int ksiz=key.length();
	result =  tcbdbout3(db_, kbuf, ksiz);
	return result;
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteKey "<<std::endl;
#endif 

}

bool DataStore::DeleteItem(const std::string &key,
    const std::string &value) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::DeleteItem "<<std::endl;
#endif 
	if ((key.size() == 0) || (value.size() == 0) )
        {
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteItem "<<std::endl;
#endif 
                return false;
        }

        bool result=false;
         // Very inefficient , deleting all values for a key and then inserting the pairs again ( removing the unwanted )
       	
	
	void *kbuf=(void*)key.c_str();
         int ksiz=key.length();
        TCLIST *L = tcbdbget4(db_, kbuf,  ksiz);
       if(L==NULL)
       	{
            	result=false;
        }
       	else
       	{
             	void *val;
             	 void *retval;
            	 int sp=0;
		 DeleteKey(key);
             	 while( (retval=tclistpop( L, &sp )) )
                {
                   	 std::string to_parse=::convert_to_string(retval,sp);
                        EncapsulatedObject obj;
                      	obj.ParseFromString(to_parse);

                       	std::string to_store=obj.data();
			boost::uint32_t value_last_published_time=obj.last_published_time();
			boost::uint32_t value_original_published_time=obj.original_published_time();
			if( to_store == value )
			{
				result=true; // found the value to delete , we are not inserting it back
			}
			else
			{
				void *key_to_store=(void*) key.c_str();
                                int key_to_store_len=key.length();
				int val_len=to_parse.length();
				void *val_to_store = (void *) to_parse.c_str();
				tcbdbputdup(db_,key_to_store,key_to_store_len,val_to_store,val_len);

			}


                }

        }
	if(L!=NULL)
	tclistdel( L ) ;
	
        
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteItem "<<std::endl;
#endif 
	return result;

		
}


bool DataStore::DeleteValue(const std::string &value) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::DeleteValue "<<std::endl;
#endif 
	void *keyval;
        BDBCUR *cur;
        if ( ! (cur = tcbdbcurnew(db_) ) )
	{
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteValue "<<std::endl;
#endif
		return false;
	
	}
        if ( !tcbdbcurfirst(cur) )
	{
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteValue "<<std::endl;
#endif
                return false;

	}
        int sp=0;
	void *val;
	
        while((val = tcbdbcurval(cur,&sp)) != NULL)
        {
               	std::string to_parse=::convert_to_string(val,sp);
                 EncapsulatedObject obj;
                 obj.ParseFromString(to_parse);
                 std::string to_test=obj.data();
		if( to_test == value )
		{
			tcbdbcurout(cur);	
		}
		else
			tcbdbcurnext(cur);

        }
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteValue "<<std::endl;
#endif 
	if(cur)
	tcbdbcurdel(cur);
        return true;
	

}

boost::uint32_t DataStore::DeleteExpiredValues() 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::DeleteExpiredValues "<<std::endl;
#endif 
	boost::uint32_t now = base::get_epoch_time();
	void *keyval;
        BDBCUR *cur;
        //cur = tcbdbcurnew(db_);
        //tcbdbcurfirst(cur);
        if ( ! (cur = tcbdbcurnew(db_) ) )
        {
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteExpiredValues"<<std::endl;
#endif
                return false;

        }
        if ( !tcbdbcurfirst(cur) )
        {
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteExpiredValues "<<std::endl;
#endif
                return false;

        }

        int sp=0;
	void *val;
	while((val = tcbdbcurval(cur,&sp)) != NULL)
        {
		std::string to_parse=::convert_to_string(val,sp);
                EncapsulatedObject obj;
                obj.ParseFromString(to_parse);
                boost::uint32_t obj_time =obj.last_published_time();
                if( obj_time < (now - kExpireTime) )
                {
			 tcbdbcurout(cur);	
                }
		else
			tcbdbcurnext(cur);
        }

#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::DeleteExpiredValues "<<std::endl;
#endif 
	if(cur)
	tcbdbcurdel(cur);
	return true;

}

boost::uint32_t DataStore::LastPublishedTime(const std::string &key,
    const std::string &value) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::LastPublishedTime "<<std::endl;
#endif 
	boost::uint32_t result=-1;
        void *kbuf=(void*)key.c_str();
        int ksiz=key.length();
        TCLIST *L = tcbdbget4(db_, kbuf,  ksiz);
        if(L==NULL)
        {
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::LastPublishedTime "<<std::endl;
#endif 
		return result;
        }
        else
        {
                void *val;
                void *retval;
                int sp=0;
                while( (result==-1) && (retval=tclistpop( L, &sp )) )
                {
			
                        std::string to_parse=::convert_to_string(retval,sp);
                        EncapsulatedObject obj;
                        obj.ParseFromString(to_parse);
                        std::string to_compare=obj.data();
			if( to_compare == value ) 
			{
				result = obj.last_published_time();
			}

                }
        }
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::LastPublishedTime "<<std::endl;
#endif 
	if(L!=NULL)
	 tclistdel( L ) ;
	return result;


}

boost::uint32_t DataStore::OriginalPublishedTime(const std::string &key,
    const std::string &value) 
{
#ifdef DEBUG
std::cout<<"DEBUG *** INSIDE Datastore::OriginalPublishedTime "<<std::endl;
#endif 
        boost::uint32_t result=-1;
        void *kbuf=(void*)key.c_str();
        int ksiz=key.length();
        TCLIST *L = tcbdbget4(db_, kbuf,  ksiz);
        if(L==NULL)
        { 
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::OriginalPublishedTime "<<std::endl;
#endif 
                return result;
        }
        else
        {
                void *val;
                void *retval;
                int sp=0;
                while( (result==-1) && (retval=tclistpop( L, &sp )) )
                {
                        std::string to_parse=::convert_to_string(retval,sp);
                        EncapsulatedObject obj;
                        obj.ParseFromString(to_parse);
                        std::string to_compare=obj.data();
                        if( to_compare == value ) 
                        {
                                result = obj.original_published_time();
                        }

                }
        }
#ifdef DEBUG
std::cout<<"DEBUG *** EXITING Datastore::OriginalPublishedTime "<<std::endl;
#endif 
	if(L!=NULL)
	 tclistdel( L ) ;
        return result;

}


}  // namespace kad
