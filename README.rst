=================
teleport-test-hbf
=================

Host based firewall using BPF and XDP

Quick Start
-----------

There are 2 ways you can use this HBF:

**VM**

You can get a VM up using `Vagrant <https://www.vagrantup.com/>`_

.. code-block::

    cd setup
    vagrant up


Now you can ssh into the host and test/ develop things.
.. code-block:: 

    vagrant ssh
    cd teleport-test-hbf
    sudo make install

    # Now you can execute the hbf:
    sudo teleport_test_hbf --help


**Container**

  Not all features are easily accessible in the containerized version yet
  
  We're using BPF ringbuffer. This feature was addedd in Linux kernel 5.8.
  Make sure your kernel version is >= 5.8

You can build the container using the Dockerfile in `setup <./setup>`_ directory

For e.g.

.. code-block:: 
  
    docker build -t mohitsharma44/hbf .


To run the container image (you need to be on a linux host to be able to run it)

.. code-block:: 

   docker-compose up


You can modify the behavior of the host based firewall by using the following environment variables:

+---------------------+-----------------------------------------------------------------------------------------+----------+
| ENV Var             | Description                                                                             | Default  |
+=====================+=========================================================================================+==========+
| HBF_IFACE           | Interface to use for monitoring incomming connections                                   | `eth0`   |
+---------------------+-----------------------------------------------------------------------------------------+----------+
| HBF_TIME_THRESHOLD  | Time threshold between which more than `HBF_MAX_PORTS` will be considered as port scan  | `5`      |
+---------------------+-----------------------------------------------------------------------------------------+----------+
| HBF_MAX_PORTS       | Maximum simultaneous connections allowed from source IP within `HBF_TIME_THRESHOLD`     | `5`      |
+---------------------+-----------------------------------------------------------------------------------------+----------+
| HBF_TIMEOUT_SECONDS | Total time to keep the HBF running                                                      | `300`    |
+---------------------+-----------------------------------------------------------------------------------------+----------+


License
--------

* Free software: `MIT license <./license>`_


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
