# <License type="Aserver BSD" version="2.0">
# 
# Copyright (c) 2005-2009, Aserver NV.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# * Neither the name Aserver nor the names of other contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ASERVER "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ASERVER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# </License>

'''View result list accessor implementation'''

class Column(object): #pylint: disable-msg=R0903
    '''Descriptor for one view row column'''
    def __init__(self, index):
        '''Create a new column accessor

        @param index: Index of the column in the result row
        @type index: number
        '''
        self.index = index

    def __get__(self, obj, objtype=None): #pylint: disable-msg=W0613
        '''Descriptor protocol __get__ implementation'''
        return obj._columns[self.index] #pylint: disable-msg=W0212

def create_row_type(description):
    '''Create a row type (class) for rows matching a given row description

    @param description: Description of all rows (name and type)
    @type description: tuple<tuple<string, string>>
    '''
    # Our final type
    class _Row(object): #pylint: disable-msg=R0903
        '''OSIS view row datatype'''
        def __init__(self, columns):
            '''Instanciate a new row

            @param columns: Column information
            @type columns: tuple<object>
            '''
            self._columns = columns

    # Generate all descriptors and set them on the row class
    for index, column in enumerate(description):
        setattr(_Row, column[0], Column(index))

    return _Row


class ViewResultList(object): #pylint: disable-msg=R0903
    '''Wrapper on top of an OSIS view result'''
    def __init__(self, list_):
        '''Generate a new view result wrapper

        @param list_: OSIS view result formatted list
        @type list_: tuple<tuple<tuple<string, string>>, tuple<tuple>>
        '''
        self._list = list_
        self._row_type = create_row_type(self._list[0])

    def __iter__(self):
        '''Iterator over the rows

        This returns a generator which returns wrapped view rows
        '''
        return (self._row_type(c) for c in self._list[1])
