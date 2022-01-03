buffer-stream-reader
====================

Naive node.js buffer stream reader

```javascript

var BufferStreamReader = require('buffer-stream-reader');
    
var buffer = new Buffer('word1 word2 word3');
var reader = new BufferStreamReader(buffer, { encoding: 'utf8' });

reader.on('readable', function onReadable () {
  while ((chunk = reader.read()) !== null) {
    console.log(chunk.toSring()); // Should print 'word1 word2 word3'
  }
});
