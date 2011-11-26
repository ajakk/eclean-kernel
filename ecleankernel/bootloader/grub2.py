#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from __future__ import print_function

import subprocess

from .grub import GRUB

grub2_autogen_header = '''#
# DO NOT EDIT THIS FILE
#
# It is automatically generated by grub2-mkconfig'''

class GRUB2(GRUB):
	name = 'grub2'
	kernel_re = r'^\s*linux\s*(\([^)]+\))?(?P<path>\S+)'
	def_path = '/boot/grub/grub.cfg'

	def _get_kernels(self, content):
		self._autogen = content.startswith(grub2_autogen_header)

		if self._autogen:
			self._debug.print('Config is autogenerated, ignoring')
			self.postrm = self._postrm
			return ()
		return GRUB._get_kernels(self, content)

	def _postrm(self):
		self._debug.print('Calling grub2-mkconfig')
		subprocess.call(['grub2-mkconfig', '-o', self.path])
