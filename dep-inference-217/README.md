# Missing dependency inference in 2.17.0rc4

This is a reproduction of an issue discovered with Pants 2.17.0rc4 where dependency inference that worked in 2.16 is failing to collect all necessary deps.

To reproduce,

``` shell
$ PANTS_VERSION=2.16.0 pants --no-verify-config test cmd::
$ pants test cmd::

```
