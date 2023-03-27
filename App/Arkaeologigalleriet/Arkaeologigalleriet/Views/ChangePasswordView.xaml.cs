using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ChangePasswordView : ContentPage
{
	public ChangePasswordView(ChangePasswordViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
	}
}