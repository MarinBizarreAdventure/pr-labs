using System;
using System.Threading.Tasks;

using lab_1.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        WebScraper webScraper = new WebScraper();
        // var (val, cur) = WebScraper.ParsePrice("25 699lei");
        //
        // Console.WriteLine($"val={val}, cur={cur}");
        string url = "https://www.cactus.md/ro/catalogue/electronice/telefone/mobilnye-telefony/";
        
        // string htmlContent = await webScraper.FetchSiteContent(url);
        
        // string htmlContentlinella = await webScraper.FetchSiteContentUsingTCP("https://linella.md/ro");
        string htmlContent = await webScraper.FetchSiteContentUsingTCP("https://www.cactus.md/ro/catalogue/electronice/telefone/mobilnye-telefony/");
        
        // Console.WriteLine(htmlContentlinella);
        
        // string htmlContent = CactusHtmlContent.cactusHtmlContent;
        // Console.WriteLine(htmlContent);
        List<ProductDetails> productDetailsList = new List<ProductDetails>();
        
        if (!htmlContent.StartsWith("Error"))
        {
            productDetailsList = webScraper.ExtractProductDetails(htmlContent);
        }
        else
        {
            Console.WriteLine(htmlContent);
        }
        
        productDetailsList[0].PrintDetails();
        var productFactory = new ProductFilterFactory(productDetailsList);
        var filteredProductDetails = productFactory.ProcessProducts(0, 100000);
        
        filteredProductDetails.PrintResults();
        
        Console.WriteLine(productDetailsList[0].SerializeToJson());
        Console.WriteLine(productDetailsList[0].SerializeToXml());
        string customSerialize = productDetailsList[0].CustomSerialize();
        Console.WriteLine(customSerialize);
        var custonDeserialize = ProductDetails.CustomDeserialize(customSerialize);
        custonDeserialize.PrintDetails();
        
    }
}

