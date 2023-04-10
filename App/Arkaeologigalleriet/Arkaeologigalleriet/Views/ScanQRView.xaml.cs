using Arkaeologigalleriet.ViewModels;
using ZXing.Net.Maui;

namespace Arkaeologigalleriet.Views;

public partial class ScanQRView : ContentPage
{
    int scannedeID;
	public ScanQRView(ScanQRViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
	}

    private async void TestQr(object sender, ZXing.Net.Maui.BarcodeDetectionEventArgs e)
    {
		if (!string.IsNullOrEmpty(e.Results[0].Value))
		{
            scannedeID = Convert.ToInt32(e.Results[0].Value);
        }
    }

    
}