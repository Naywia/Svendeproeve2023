using Arkaeologigalleriet.ViewModels;
using ZXing.Net.Maui;

namespace Arkaeologigalleriet.Views;

public partial class ScanQRView : ContentPage
{
	public ScanQRView(ScanQRViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
	}

    private void TestQr(object sender, ZXing.Net.Maui.BarcodeDetectionEventArgs e)
    {
		Dispatcher.Dispatch(() =>
		{
			QRLabel.Text = e.Results[0].Value;


        });
    }
}