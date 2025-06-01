// SPDX-License-Identifier: SIIT
pragma solidity ^0.8.0;

contract LicenseDataStore {
    struct Context {
        string password;
        string otp;
        string fingerprint;
    }

    // Mapping from license number to context data
    mapping(string => Context) private dataStore;

    // Public function to manually add or update context data
    function setContext(
        string memory licensenumber,
        string memory password,
        string memory otp,
        string memory fingerprint
    ) public {
        dataStore[licensenumber] = Context(password, otp, fingerprint);
    }

    // Get stored password by license number
    function getPassword(string memory licensenumber) public view returns (string memory) {
        return dataStore[licensenumber].password;
    }

    // Get stored OTP by license number
    function getOtp(string memory licensenumber) public view returns (string memory) {
        return dataStore[licensenumber].otp;
    }

    // Get stored fingerprint method by license number
    function getFingerprint(string memory licensenumber) public view returns (string memory) {
        return dataStore[licensenumber].fingerprint;
    }
}
