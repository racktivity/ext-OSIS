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

from .model import Model, RootObjectModel
__all__ = ['Model', 'RootObjectModel', ]

#Load all types
def _install():
    import logging
    logger = logging.getLogger('osis.model')
    logger.info('Installing field types')

    import inspect

    import osis.model.fields
    from osis.model.fields import ExposedField
    field_mod = inspect.getmodule(ExposedField)

    glob = globals()

    #Load all exposed Field types
    logger.debug('Loading field types')
    for attr_name in (name for name in dir(field_mod) if not
            name.startswith('_')):
        attr = getattr(field_mod, attr_name)
        if inspect.isclass(attr) and issubclass(attr, ExposedField) \
           and attr is not ExposedField:
            logger.debug('Found field type %s' % attr_name)
            if attr_name in glob:
                raise RuntimeError('%s already defined' % attr_name)
            glob[attr_name] = attr
            __all__.append(attr_name)

    #Clean up module, so tab completion is nice and shiny
    logger.debug('Cleaning up package globals')
    for name, value in glob.copy().iteritems():
        if name.startswith('__'):
            continue

        if inspect.isclass(value) and issubclass(value, ExposedField) \
           and value is not ExposedField:
            continue

        if value in (Model, RootObjectModel, ):
            continue

        glob.pop(name)

_install()
