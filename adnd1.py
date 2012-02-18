"""
First edition Character
"""
from tes import rnd
class Character:
    def firstupper(f):
        def _firstupper(*args,**kw):
            r=f(*args,**kw)
            # capitalize first letter
            return r.title()
        _firstupper.__doc__=f.__doc__
        return _firstupper
    @firstupper
    def name(self,name='spartacus'):
        """
	>>> Character().name()
        'Spartacus'
        >>> x=Character()
        >>> x.name("laszo")
        'Laszo'
        >>> x.name()
        'Laszo'
        """
	try:
		self._name
	except:
        	self._name=name
        return self._name
    def level(self,value=1):
        try:
		self._level
        except:
		self._level=value
	return  self._level
    def hitdice(self,value=8):
	try:
		self._hitdice
	except:
		self._hitdice=value
	return self._hitdice
    def hp(self):
        try:
		self._pf_progression
	except:
		self._pf_progression=[rnd(1,self.hitdice()) for i in range(0,self.level())]
	return reduce(lambda x, y: x+y, self._pf_progression)
if __name__=='__main__':
    import doctest
    doctest.testmod()

