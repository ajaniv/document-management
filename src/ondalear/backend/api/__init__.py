"""
.. module::  ondalear.backend.docmgmt.api
   :synopsis: document management api package.

This package contains server Django api abstractions.

"""
 # @TODO: can check reqeust header to determine whether a short response (i.e id only)
 # is desired for  put/post requestd
 # @TODO: For put and post requests, the serializer is 'doing the hard' work to only return id
 #  when short response is required
 