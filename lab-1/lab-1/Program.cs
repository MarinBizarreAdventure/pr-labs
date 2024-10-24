using System;
using System.Threading.Tasks;

using lab_1.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        GetRequest getRequest = new GetRequest();

        string url = "https://www.cactus.md/ru/catalogue/electronice/telefone/mobilnye-telefony/";

        string htmlContent = await getRequest.FetchSiteContent(url);
        
        Console.WriteLine(htmlContent);
    }
}

