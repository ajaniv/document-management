## Authorization
* Need to log in using the user-admin api login end point to obtain token
* Then authorize by setting the token (i.e. `Token 5378d55fb8173d1b4f7fa17457d29566fd7d4b3a`), 
  at which point the  api endpoints can be used.
* One can use the logout and login swagger multiple times to switch user
  after obtaining a diffrent token.

# Issues
* Document data needs to be flattened.  This is due to the multi-part not handling
  nested data
* Not seeing file upload option for ReferenceDocument, AuxiliaryDocument