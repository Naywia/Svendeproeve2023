using Arkaeologigalleriet.Services;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(UserID), nameof(UserID))]
    public partial class ChangePasswordViewModel : INotifyPropertyChanged
    {

        #region Propertys

        
        ApiServices Api = new();

        private int _userID;

        public int UserID
        {
            get { return _userID; }
            set 
            { 
                _userID = value;
                OnPropertyChanged(nameof(UserID));
            }
        }

        private string _oldPassword;

        public string OldPassword
        {
            get { return _oldPassword; }
            set 
            {
                _oldPassword = value;
                OnPropertyChanged(nameof(OldPassword));
            }
        }

        private string _newPassword;

        public string NewPassword
        {
            get { return _newPassword; }
            set 
            {
                _newPassword = value;
                OnPropertyChanged(nameof(NewPassword));
            }
        }

        private string _repeatPassword;

        public string RepeatPassword
        {
            get { return _repeatPassword; }
            set 
            { 
                _repeatPassword = value;
                OnPropertyChanged(nameof(RepeatPassword));
            }
        }
        #endregion

        public ChangePasswordViewModel()
        {
            
        }

        [RelayCommand]
        public async Task<bool> CheckPassword()
        {
            if (NewPassword == RepeatPassword)
            {
                
                if (await UpdateNewPassword())
                {
                    await Application.Current.MainPage.DisplayAlert("Opadteret", "Din kode er nu opdateret", "Ok");
                    await Shell.Current.GoToAsync("..");
                    return true;
                }
                
            }
            else
            {
                await Application.Current.MainPage.DisplayAlert("Fejl", "Gammel password stemmer ikke overens", "Ok");
                return false;
            }
            return false;
        }

        public async Task<bool> UpdateNewPassword()
        {
            if (await Api.Changepassword(UserID, OldPassword, NewPassword, RepeatPassword))
            {
                return true;
            }
            else
            {
                await Application.Current.MainPage.DisplayAlert("Fejl", "Noget gik galt. Prøv igen", "Ok");
                return false;
            }
        }

        [RelayCommand]
        public async void Annuller()
        {
            await Shell.Current.GoToAsync("..");
        }
        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
