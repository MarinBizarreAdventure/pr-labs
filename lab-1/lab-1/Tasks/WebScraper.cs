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

            var linkNode = productNode.SelectSingleNode(".//a[@href]");

            if (nameNode != null && priceNode != null && linkNode != null)
            {
                string productName = nameNode.InnerText.Trim();
                string priceText = priceNode.InnerText.Trim();
                string productLink = "https://www.cactus.md" + linkNode.GetAttributeValue("href", string.Empty);
                
                (int productPriceAmount, string productPriceCurrency) = ParsePrice(priceText);

                var parameters = ScrapeProductDetailsFromLink(productLink).Result;
                
                var productDetails = new ProductDetails(productName, productPriceCurrency, productPriceAmount,  productLink, parameters);
                
                Console.WriteLine($"Product: {productName}, price:{productPriceAmount} {productPriceCurrency}, link:{productLink}");
            }
            
        }
    }

    public async Task<Dictionary<string, string>> ScrapeProductDetailsFromLink(string productUrl)
    {
        try
        {
            string htmlContent = await FetchSiteContent(productUrl);
            if (string.IsNullOrEmpty(htmlContent))
            {
                Console.WriteLine("No HTML content fetched.");
                return null;
            }

            HtmlDocument htmlDocument = new HtmlDocument();
            htmlDocument.LoadHtml(htmlContent);

            var productNode = htmlDocument.DocumentNode.SelectSingleNode("//div[@class='catalog__item__panel' and @itemscope and @itemtype='http://schema.org/Product']");

            if (productNode != null)
            {
                var parametersDiv = productNode.SelectSingleNode(".//div[@id='ctl00_cphMain_divParameters']");

                if (parametersDiv != null)
                {
                    var parameterNodes = parametersDiv.SelectNodes(".//ul/li");
                    var parameters = new Dictionary<string, string>();

                    foreach (var parameterNode in parameterNodes)
                    {
                        var titleNode = parameterNode.SelectSingleNode(".//h2[@class='catalog__characteristic__title']");
                        if (titleNode != null)
                        {
                            string title = titleNode.InnerText.Trim();

                            var unitNode = parameterNode.SelectSingleNode(".//span[@class='catalog__characteristic__unit']");
                            string unit = unitNode != null ? unitNode.InnerText.Trim() : string.Empty;

                            parameters[title] = unit;
                        }
                    }

                    foreach (var param in parameters)
                    {
                        Console.WriteLine($"{param.Key}: {param.Value}");
                    }

                    return parameters; 
                }
                else
                {
                    Console.WriteLine("Parameters div not found.");
                }
            }
            else
            {
                Console.WriteLine("Product node not found.");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error fetching product details: {ex.Message}");
        }

        return null; 
    }

    private static (int, string) ParsePrice(string priceText)
    {
        int lastSpaceIndex = priceText.LastIndexOf(' ');
        string amountText = priceText.Substring(0, lastSpaceIndex);
        string currency = priceText.Substring(lastSpaceIndex + 1);

        int amount = int.Parse(amountText.Replace(" ", ""));
        
        return (amount, currency);
    }
    
    
}