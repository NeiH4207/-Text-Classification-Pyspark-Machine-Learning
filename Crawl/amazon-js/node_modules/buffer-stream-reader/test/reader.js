var must = require('must');
var demand = must;

var BufferStreamReader = require('../reader');

describe('BufferStreamReader', function () {
  it('should read chunks of data', function (done) {
    var buffer = new Buffer('word1 word2 word3');
    var reader = new BufferStreamReader(buffer, {
      encoding: 'utf8',
      chunkSize: 5,
      highWaterMark: 32
    });

    reader.on('readable', function onReadable () {
      demand(reader.read()).to.eql('word1 word2 word3');
      done();
    });
  });
});