using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Maui.Core.Extensions;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;

namespace Arkaeologigalleriet.ViewModels
{
    
    public partial class SearchViewModel : BaseViewModel
    {
        #region Propyties

        HttpClient _client;
        //string _url = "http://192.168.1.100:8000/";
        string _url = "http://164.68.113.72:8000/";

        


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

        private List<Artefact> _savedList;
        #endregion



        public SearchViewModel()
        {

        }



        public async void GetAllArtefacts()
        {
            Models = new List<ArtifactInformationModels>();
            Artefacts = new ObservableCollection<Artefact>();
            _savedList = new List<Artefact>();
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
                            _savedList.Add(item);
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

        

        [RelayCommand]
        public async void Tapped(object item)
        {
            var id = (item as Artefact).ID;
            await Shell.Current.GoToAsync($"{nameof(ArtifactInformationView)}?ArtifactID={id}");
        }

        [RelayCommand]
        public async void FilterSearch(object keyword)
        {
            try
            {
                var input = (keyword as string);
                if (!string.IsNullOrEmpty(input))
                {
                    Artefacts.Clear();
                    var data = _savedList.Where(i => i.Name.ToLower().Contains(input.ToLower())).ToList();
                    
                    foreach (var item in data)
                    {
                        Artefacts.Add(item);
                    }
                }
                else
                {
                    Artefacts = _savedList.ToObservableCollection();
                }
            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
               
            }
            
        }
    }
}
