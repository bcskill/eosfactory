
#include <stdlib.h>
#include <string>
#include <iostream>


#include <fc/crypto/base58.hpp>
#include <fc/crypto/elliptic.hpp>
#include <fc/io/raw.hpp>
#include <fc/crypto/hmac.hpp>
#include <fc/crypto/openssl.hpp>
#include <fc/crypto/ripemd160.hpp>

#include <eos/utilities/key_conversion.hpp>
#include <fc/crypto/base58.hpp>
#include <fc/variant.hpp>

using namespace std;

int main()
{
  auto privateKey = fc::ecc::private_key::generate();
  string key = eosio::utilities::key_to_wif(privateKey.get_secret());
  cout << key << endl;

}

