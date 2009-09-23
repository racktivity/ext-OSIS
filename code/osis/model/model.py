import logging
import weakref
import inspect

from osis.model.fields import Field, GUID, String

logger = logging.getLogger('osis.model')

GUIDField = GUID()
GUIDField.name = 'guid'
VersionField = GUID()
VersionField.name = 'version'
CreationDateField = String()
CreationDateField.name = 'creationdate'
DEFAULT_FIELDS = (GUIDField, VersionField, CreationDateField, )

class _OsisModelAttribute(object):
        def __init__(self, name, attribute):
            self.name = name
            self.attribute = attribute

class _OsisModelInfo(object):
    def __init__(self, name, attrs):
        self.type = None
        self.name = name

        self.read_attributes(attrs)

    def read_attributes(self, attrs):
        logger.debug('Creating attribute info for %s' % self.name)
        self.attributes = tuple(_OsisModelAttribute(*info) for info in
                attrs.iteritems() if isinstance(info[1], Field))


    def __str__(self):
        return 'OSIS model info for %s' % self.name


    def get_name(self):
        return self.name



class ModelMeta(type):
    def __new__(cls, name, bases, attrs, allow_slots=False):
        logger.info('Generating model type %s' % name)
        try:
            Model
            RootObjectModel
        except NameError:
            return type.__new__(cls, name, bases, attrs)

        if not allow_slots and '__slots__' in attrs:
            raise RuntimeError(
                'Don\'t set a \'__slots__\' value on model classes')

        assert 'guid' not in attrs, \
                'Model classes should have no explicit \'guid\' attribute'
        assert 'version' not in attrs, \
                'Model classes should have no explicit \'version\' attribute'
        assert 'creationdate' not in attrs, \
                'Model classes should have no explicit' \
                'creationdate\' attribute'

        for field in DEFAULT_FIELDS:
            attrs[field.name] = field

        attrs['OSIS_MODEL_INFO'] = _OsisModelInfo(name, attrs)

        for attr_name, attr in attrs.iteritems():
            if isinstance(attr, Field) and attr not in DEFAULT_FIELDS:
                attr.name = attr_name

        import osis.model
        extra_bases = set(bases).difference(
            set((osis.model.Model, osis.model.RootObjectModel, )))
        if extra_bases:
            raise RuntimeError(
                'A model should only inherit from Model or RootObjectModel, '
                'not %s' % repr([base.__name__ for base in extra_bases]))

        for base in bases:
            if not hasattr(base, '__slots__'):
                raise RuntimeError('Base class %s has no __slots__ defined' %
                                   base.__name__)

        # Calculate and set __slots__ - see 'Datamodel' in the Python
        # language reference
        slots = ['_osis_store', ]
        for attrname, attr in attrs.iteritems():
            if isinstance(attr, Field):
                slots.append(attrname)
        attrs['__slots__'] = tuple(slots)

        type_ = type.__new__(cls, name, bases, attrs)
        # Do we actually need this?
        type_.OSIS_MODEL_INFO.type = weakref.proxy(type_)

        # Perform one more __slots__ check, just to be sure (other metaclasses
        # might fool us)
        for base in inspect.getmro(type_):
            if base is not object and not hasattr(base, '__slots__'):
                raise RuntimeError('Base class %s has no __slots__ defined' % \
                                   base.__name__)

        return type_


class Model(object):
    __metaclass__ = ModelMeta
    __slots__ = ('_osis_store', )

    # Make PyLint happy, set by metaclass
    OSIS_MODEL_INFO = None

    def __init__(self, **kwargs):
        self._osis_store = dict()

        attribute_names = set(attr.name for attr in
                self.OSIS_MODEL_INFO.attributes)

        for key, value in kwargs.iteritems():
            if key not in attribute_names:
                raise ValueError('Unknown attribute %s' % key)

            setattr(self, key, value)

    def __str__(self):
        d = dict()
        for attr in self.OSIS_MODEL_INFO.attributes:
            d[attr.name] = getattr(self, attr.name)

        return str(d)

    def __eq__(self, other):
        if self is other:
            return True

        if not type(self) is type(other):
            return NotImplemented

        if not self.version or not self.guid:
            return False

        return self.guid == other.guid and self.version == other.version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if not self.version:
            return hash(self.guid) if self.guid else object.__hash__(self)

        return hash((self.guid, self.version, ))


class RootObjectModel(Model):
    __slots__ = tuple()

    def serialize(self, serializer):
        return serializer.serialize(self)

    @classmethod
    def deserialize(cls, deserializer, data):
        return deserializer.deserialize(cls, data)
