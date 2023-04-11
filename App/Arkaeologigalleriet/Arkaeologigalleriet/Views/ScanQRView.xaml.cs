using Arkaeologigalleriet.ViewModels;
using CommunityToolkit.Maui.Core.Views;
using ZXing.Net.Maui;

namespace Arkaeologigalleriet.Views;

public partial class ScanQRView : ContentPage
{
    private readonly ScanQRViewModel _vm;

    public ScanQRView(ScanQRViewModel vm)
    {
        InitializeComponent();
        BindingContext = vm;
        _vm = vm;
    }

    [Obsolete]
    private async void TestQr(object sender, ZXing.Net.Maui.BarcodeDetectionEventArgs e)
    {

        if (!string.IsNullOrEmpty(e.Results[0].Value))
        {

            barcodeReader.IsDetecting = false;
            ArtifactInformationViewModel artifactInformationViewModel = new ArtifactInformationViewModel();
            try
            {
                Device.BeginInvokeOnMainThread(async () =>
                {
                    await Shell.Current.GoToAsync($"{nameof(ArtifactInformationView)}?ArtifactID={e.Results[0].Value}");
                });

            }
            catch (Exception ex)
            {

                await DisplayAlert("Fejl", ex.Message, "OK");
            }
           
        }
    }

    private void AtivateScanBtn(object sender, EventArgs e)
    {
        barcodeReader.IsDetecting = true;
    }
}