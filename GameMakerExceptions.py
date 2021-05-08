# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Developpers : Antoine D., Kernel
# GameMaker module -- exceptions

class UserStoneOverwriteError(Exception):

    def __init__(self,message="Can't place this stone at this intersection"):
        super().__init__(message)

class TooFarFromIntersectionWarning(Exception):

    def __init__(self,message="Click position is too far from an intersection"):
        super().__init__(message)

class CreateNewStoneGroupSignal(Exception):

	def __init__(self, stone):
		self.init_member = [stone]

	def __str__(self):
		return 'signal : create group with {}'.format(self.init_member)