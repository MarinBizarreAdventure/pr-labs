using System;
using System.Threading.Tasks;

using lab_1.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        WebScraper webScraper = new WebScraper();

        string url = "https://www.cactus.md/ro/catalogue/electronice/telefone/mobilnye-telefony/";

        // string htmlContent = await webScraper.FetchSiteContent(url);

        string htmlContentlinella = await webScraper.FetchSiteContentUsingTCP("https://linella.md/ro");
        Console.WriteLine(htmlContentlinella);

        // string htmlContent = CactusHtmlContent.cactusHtmlContent;
        // // Console.WriteLine(htmlContent);
        // List<ProductDetails> productDetailsList = new List<ProductDetails>();
        //
        // if (!htmlContent.StartsWith("Error"))
        // {
        //     productDetailsList = webScraper.ExtractProductDetails(htmlContent);
        // }
        // else
        // {
        //     Console.WriteLine(htmlContent);
        // }
        //
        // var productFactory = new ProductFilterFactory(productDetailsList);
        // var filteredProductDetails = productFactory.ProcessProducts(100, 500);
        //
        // filteredProductDetails.PrintResults();

    }
}

