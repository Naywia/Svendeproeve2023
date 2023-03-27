using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ScanQRView : ContentPage
{
	public ScanQRView(ScanQRViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
	}
}