/**
 * @module BufferStreamReader
 */
var stream = require('stream');

/**
 * Create a new stream reader
 *
 * @param data
 * @param options
 * @returns {StringReader}
 *
 * @constructor
 */
function BufferStreamReader (data, options) {
  if (!(this instanceof BufferStreamReader)) {
    return new BufferStreamReader(data);
  }

  if (!options) {
    options = {};
  }

  stream.Readable.call(this, options);

  this._data = null;
  this._chunkSize = options.chunkSize || -1;

  if (typeof data === 'string') {
    this._data = new Buffer(data, options.encoding || 'utf8');
  } else if (Buffer.isBuffer(data)) {
    this._data = data;
  }
}

/**
 * Derive from stream.Readable prototype
 */
BufferStreamReader.prototype = Object.create(stream.Readable.prototype, {
  constructor: { value: BufferStreamReader }
});

/**
 * Implement _read
 *
 * @param size
 * @private
 */
BufferStreamReader.prototype._read = function _read (size) {
  if (!this._data) {
    return this.push(null);
  }

  var canRead = true;
  var data = this._data;
  var bytesToRead = data.length;
  var chunkSize = this._chunkSize > 0 ? this._chunkSize : size;

  while (canRead) {
    var read = Math.min(chunkSize, bytesToRead);
    var buf = data.slice(0, read);

    this.push(buf);
    bytesToRead -= read;

    if (bytesToRead <= 0) {
      canRead = false;

      delete data;
      return this.push(null);
    }

    data = data.slice(read, data.length);
  }
};

module.exports = BufferStreamReader;