using Arkaeologigalleriet.Models;
using CommunityToolkit.Mvvm.ComponentModel;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(ArtifactID), nameof(ArtifactID))]
    public partial class ArtifactInformationViewModel : ObservableObject
    {
        HttpClient _client;
        string _url = "http://192.168.1.100:8000/";

        [ObservableProperty]
        ArtifactInformationModel _artifactInformationModel;

        [ObservableProperty]
        int artifactID;

        public ArtifactInformationViewModel()
        {
            _artifactInformationModel = new ArtifactInformationModel();
        }

        

        public async Task<ArtifactInformationModel> GetArtifact()
        {
            
            //_client = new HttpClient();

            //try
            //{
            //    using HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, _url + "artefact?artefactID=" + artifactID);
            //    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
            //    HttpResponseMessage response = await _client.SendAsync(request);
            //    if (response.IsSuccessStatusCode)
            //    {
            //        string payload = await response.Content.ReadAsStringAsync();
            //        try
            //        {
            //            var jsonModel = JsonConvert.DeserializeObject<ArtifactInformationModel>(payload);
            //            model = jsonModel;
            //        }
            //        catch (Exception ex)
            //        {
            //            Console.Out.WriteLine(ex.Message);
            //            throw;
            //        }
            //        return model;
            //    }
            //}
            //catch (Exception ex)
            //{
            //    Console.Out.WriteLine(ex.Message);
            //    throw;
            //}


            //return null;

            _artifactInformationModel.Name = "Starry Night Over the Rhone";
            _artifactInformationModel.Description = "Kunstner: Vincent van Gogh\nDato: 1888\nMedium: Olie på lærred\\nStørrelse: 72,5 x 92 cm\n\nVincent van Gogh, en af ??de mest berømte malere i historien, malede'Starry Night Over the Rhone' i 1888. Dette maleri viser en natlig scene langs Rhône-floden i Arles, Frankrig, hvor van Gogh boede på det tidspunkt. Billedet viser en stjerneklar nattehimmel, der reflekterer i vandet på Rhône-floden. To figurer kan ses på kanten af ??floden, mens en båd sejler forbi i baggrunden. Van Gogh brugte levende farver og børstestrøg for at skabe en intens og drømmende stemning i maleriet. 'Starry Night Over the Rhone' er en af ??van Goghs mest ikoniske værker og er nu en del af samlingen på Musée d'Orsay i Paris.";
            _artifactInformationModel.ArtefactType = "Glas flaske";
            _artifactInformationModel.Storage = "Lager Syd";
            _artifactInformationModel.Shelf = 1;
            _artifactInformationModel.Row = "A";

            return _artifactInformationModel;
        }

        
    }
}
//Test.Text = "Title: Starry Night Over the Rhone\nKunstner: Vincent van Gogh\nDato: 1888\nMedium: Olie på lærred\nStørrelse: 72,5 x 92 cm\n\nVincent van Gogh, en af ??de mest berømte malere i historien, malede'Starry Night Over the Rhone' i 1888. Dette maleri viser en natlig scene langs Rhône-floden i Arles, Frankrig, hvor van Gogh boede på det tidspunkt. Billedet viser en stjerneklar nattehimmel, der reflekterer i vandet på Rhône-floden. To figurer kan ses på kanten af ??floden, mens en båd sejler forbi i baggrunden. Van Gogh brugte levende farver og børstestrøg for at skabe en intens og drømmende stemning i maleriet. 'Starry Night Over the Rhone' er en af ??van Goghs mest ikoniske værker og er nu en del af samlingen på Musée d'Orsay i Paris.";