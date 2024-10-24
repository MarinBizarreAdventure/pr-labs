namespace lab_1.Tasks;
using System;
using System.Net.Http;
using System.Threading.Tasks;
using HtmlAgilityPack;

public class WebScraper
{
    private readonly HttpClient _httpClient;

    public WebScraper()
    {
        _httpClient = new HttpClient();
    }

    public async Task<string> FetchSiteContent(string url)
    {
        try
        {
            HttpResponseMessage response = await _httpClient.GetAsync(url);

            if (response.IsSuccessStatusCode)
            {
                string htmlContent = await response.Content.ReadAsStringAsync();
                return htmlContent;
            }
            else
            {
                return $"Error: Unable to fetch the website. StatusCode: {response.StatusCode}";
            }
        }
        catch (Exception ex)
        {
            return $"Exception: {ex.Message}";
        }
    }

    public void ExtractProductDetails(string htmlContent)
    {
        var htmlDocument = new HtmlDocument();
        htmlDocument.LoadHtml(htmlContent);

        var productNodes = htmlDocument.DocumentNode.SelectNodes("//div[@class='catalog__pill']");

        if (productNodes == null)
        {
            Console.WriteLine("No products are found");
            return;
        }

        foreach (var productNode in productNodes)
        {
            var nameNode = productNode.SelectSingleNode(".//span[@class='catalog__pill__text__title']");

            var priceNode = productNode.SelectSingleNode(".//div[@class='catalog__pill__controls__price']");

            if (nameNode != null && priceNode != null)
            {
                string productName = nameNode.InnerText.Trim();
                string productPrice = priceNode.InnerText.Trim();
                
                Console.WriteLine($"Product: {productName}, price:{productPrice}");
            }
            
        }
        
    }

}