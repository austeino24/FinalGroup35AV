// Auto-generated. Do not edit!

// (in-package mynt_eye_ros_wrapper.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class GetInfoRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.key = null;
    }
    else {
      if (initObj.hasOwnProperty('key')) {
        this.key = initObj.key
      }
      else {
        this.key = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetInfoRequest
    // Serialize message field [key]
    bufferOffset = _serializer.uint32(obj.key, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetInfoRequest
    let len;
    let data = new GetInfoRequest(null);
    // Deserialize message field [key]
    data.key = _deserializer.uint32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'mynt_eye_ros_wrapper/GetInfoRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fa0a47488b1470723cd32a81b6fdd5e2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 DEVICE_NAME=0
    uint32 SERIAL_NUMBER=1
    uint32 FIRMWARE_VERSION=2
    uint32 HARDWARE_VERSION=3
    uint32 SPEC_VERSION=4
    uint32 LENS_TYPE=5
    uint32 IMU_TYPE=6
    uint32 NOMINAL_BASELINE=7
    
    uint32 key
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetInfoRequest(null);
    if (msg.key !== undefined) {
      resolved.key = msg.key;
    }
    else {
      resolved.key = 0
    }

    return resolved;
    }
};

// Constants for message
GetInfoRequest.Constants = {
  DEVICE_NAME: 0,
  SERIAL_NUMBER: 1,
  FIRMWARE_VERSION: 2,
  HARDWARE_VERSION: 3,
  SPEC_VERSION: 4,
  LENS_TYPE: 5,
  IMU_TYPE: 6,
  NOMINAL_BASELINE: 7,
}

class GetInfoResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.value = null;
    }
    else {
      if (initObj.hasOwnProperty('value')) {
        this.value = initObj.value
      }
      else {
        this.value = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetInfoResponse
    // Serialize message field [value]
    bufferOffset = _serializer.string(obj.value, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetInfoResponse
    let len;
    let data = new GetInfoResponse(null);
    // Deserialize message field [value]
    data.value = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.value.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'mynt_eye_ros_wrapper/GetInfoResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '64e58419496c7248b4ef25731f88b8c3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string value
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetInfoResponse(null);
    if (msg.value !== undefined) {
      resolved.value = msg.value;
    }
    else {
      resolved.value = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: GetInfoRequest,
  Response: GetInfoResponse,
  md5sum() { return '56f133f7e0c9921bec0c0503f4bdd24d'; },
  datatype() { return 'mynt_eye_ros_wrapper/GetInfo'; }
};
