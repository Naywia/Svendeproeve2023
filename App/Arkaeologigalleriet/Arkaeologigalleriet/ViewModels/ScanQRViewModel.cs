using Arkaeologigalleriet.Views;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class ScanQRViewModel : ObservableObject
    {
        int id = 1;
        [RelayCommand]
        Task Navigate() => Shell.Current.GoToAsync($"{nameof(ArtifactInformationView)}?ID={id}");
    }
}
