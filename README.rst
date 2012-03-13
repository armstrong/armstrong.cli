armstrong.cli
=============
Provides basic commands needed for Armstrong scaffolding

Usage
-----

armstrong.cli is used as the entry point for all armstrong specific commands as
well as being a replacement for the django manage.py script. The base package
provides the init command which will create a new armstrong project at a
given path.

To create additional armstrong commands, create a callable and specify it as an
'armstrong.command' entry_point via setuptools. If the command can be run
outside of the context of an armstrong project, the callable should have the
attribute ``requires_armstrong`` set to false. Additionally, if the command
takes argument, a subparser from ``argparse`` will be passed to the optional
``build_parser`` method of your command.


Installation
------------
We recommend installing this through pypi.  You can install it like this::

    pip install armstrong.cli


Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `pull request`_

.. _Fork it: http://help.github.com/forking/
.. _pull request: http://help.github.com/pull-requests/


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_, and a grant from the `John S. and James L. Knight
Foundation`_.  The first release is scheduled for June, 2011.

To follow development, be sure to join the `Google Group`_.

``armstrong.cli`` is part of the `Armstrong`_ project.  You're
probably looking for that.

.. _Texas Tribune: http://www.texastribune.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Google Group: http://groups.google.com/group/armstrongcms
.. _Armstrong: http://www.armstrongcms.org/


License
-------
Copyright 2011 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
