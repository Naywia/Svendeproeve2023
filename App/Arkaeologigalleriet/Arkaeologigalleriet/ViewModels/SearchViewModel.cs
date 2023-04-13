using Arkaeologigalleriet.Models;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class SearchViewModel : INotifyPropertyChanged
    {
        #region Propyties

        HttpClient _client;
        string _url = "http://192.168.1.100:8000/";

        private List<ArtifactInformationModels> _models;

        public List<ArtifactInformationModels> Models
        {
            get { return _models; }
            set
            {
                _models = value;
                OnPropertyChanged(nameof(Models));
            }
        }

        private ObservableCollection<Artefact> _artefacts;

        public ObservableCollection<Artefact> Artefacts
        {
            get { return _artefacts; }
            set
            {
                _artefacts = value;
                OnPropertyChanged(nameof(Artefacts));
            }
        }


        #endregion



        public SearchViewModel()
        {

        }



        public async void GetAllArtefacts()
        {
            Models = new List<ArtifactInformationModels>();
            Artefacts = new ObservableCollection<Artefact>();
            _client = new HttpClient();

            

            try
            {
                using HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, _url + "artefact");
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                HttpResponseMessage response = await _client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {
                        var jsonmodel = JsonConvert.DeserializeObject<ArtifactInformationModels>(payload);
                        Models.Add(jsonmodel);
                        foreach (var item in jsonmodel.Artefacts)
                        {                            
                            Artefacts.Add(item);
                        }


                    }
                    catch (Exception ex)
                    {
                        await Console.Out.WriteLineAsync(ex.Message);
                        throw;
                    }
                }
            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
                throw;
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        
        public void Test(Artefact artefact)
        {
            var Test = artefact;
            string testy = Test.ID.ToString();
        }
    }
}
