using System;
using System.Threading.Tasks;

using lab_1.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        WebScraper webScraper = new WebScraper();

        string url = "https://www.cactus.md/ro/catalogue/electronice/telefone/mobilnye-telefony/";

        string htmlContent = await webScraper.FetchSiteContent(url);
        
        // Console.WriteLine(htmlContent);
            
        if (!htmlContent.StartsWith("Error"))
        {
            webScraper.ExtractProductDetails(htmlContent);
        }
        else
        {
            Console.WriteLine(htmlContent);
        }
        

        // var details = await webScraper.ScrapeProductDetailsFromLink(
        //     "https://www.cactus.md/ro/catalogue/electronice/telefone/mobilnye-telefony/allview-d3-senior-duos-black/");
        
         

        // Console.WriteLine(htmlContent);
    }
}

