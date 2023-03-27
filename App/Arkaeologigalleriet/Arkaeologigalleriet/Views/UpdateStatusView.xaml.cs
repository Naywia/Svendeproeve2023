using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class UpdateStatusView : ContentPage
{
	public UpdateStatusView(UpdateStatusViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
	}
}