const amazonScraper = require('amazon-buddy');
const fs = require('fs');

function appendFile(data) {
    fs.appendFile('reviewData.json',data, function(err) {
        if (err) return console.log(err);
    });
} 

async function runJob() {
    // crawl asin
    var asinList =["B01GW3H3U8"];
    (async () => {
        try {
            asinList.forEach(async ( asin ) => {
                try {
                    const reviews = await amazonScraper.reviews({ asin: asin, number: 2000});
                    var results = reviews.result
                    // console.log(reviews.result.length)

                    results.forEach(result => {
                        result.asin = result.asin.original;
                        result.reviewTime = new Date(result.date.unix*1000).toLocaleDateString("en-US").replace(/\//g, "-");
                        result.overall = result.rating;
                        result.verified = result.verified_purchase;
                        result.reviewText = result.review;
                        result.reviewTitle = result.title;
                        result.reviewerID = result.id;
                        result.reviewerName = result.name;
                        result.summary = result.title;
                        result.unixReviewTime = result.date.unix;

                        delete result.id
                        delete result.review_data
                        delete result.date
                        delete result.name
                        delete result.rating
                        delete result.title
                        delete result.review
                        delete result.verified_purchase

                        result = JSON.stringify(result, null, 0) + "\n";
                        appendFile(result)
                    })
                }catch(err) {
                    console.log(err)
                }
            })
        }catch (err) {
            console.log(err)
        }

    })()
}

runJob()

async function getAsin() {
    const products = await amazonScraper.products({ keyword: 'shirt', number: 200 });
    var asinList = [];
    products.result.forEach(product => {
        asinList.push(product.asin)
    })
    var file = fs.createWriteStream('asin.json');
    file.on('error', function(err) { /* error handling */ });
    var a = { asins: asinList }
    file.write(JSON.stringify(a, null, 2));
    file.end();

}
// getAsin()