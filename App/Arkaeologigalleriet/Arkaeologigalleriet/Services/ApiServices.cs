using Arkaeologigalleriet.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Services
{
    public class ApiServices
    {
        HttpClient _client = new HttpClient();
        string _url = "http://192.168.1.100:8000/";

        #region UpdateEmp

        
        public async Task<bool> UpdateEmpInfo(EmployeeModel model)
        {
            int empId = await GetEmployeeTypeID(model.EmployeeType);
            UpdateEmployeeModel update= new UpdateEmployeeModel() 
            {
                FirstName = model.FirstName,
                LastName = model.LastName,
                Email = model.Email,
                PhoneNumber = model.PhoneNumber,
                Address = model.Address,
                Postal = model.Postal,
                EmployeeTypeID = empId,
            };

            
            
            try
            {
                using HttpRequestMessage requestMessage = new HttpRequestMessage(HttpMethod.Patch, _url + "user?userID=" + model.ID);
                requestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                
                requestMessage.Content = JsonContent.Create(update);
                HttpResponseMessage response = await _client.SendAsync(requestMessage);
                if (response.IsSuccessStatusCode)
                {
                    return true;
                }
                
            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
                
            }
            return false;
        }

        private async Task<int> GetEmployeeTypeID(string EmployeeType)
        {
            EmpTypeModel empTypeModel = new EmpTypeModel();
            EmpRoot empRoot = new();
            try
            {
                using HttpRequestMessage requestMessage = new HttpRequestMessage(HttpMethod.Get, _url + "employeeType");
                requestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                HttpResponseMessage response = await _client.SendAsync(requestMessage);
                if (response.IsSuccessStatusCode)
                {
                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {
                        var jsonModel = JsonConvert.DeserializeObject<EmpRoot>(payload);
                        empRoot = jsonModel;
                        foreach (var item in jsonModel.empType)
                        {
                            empTypeModel = item;
                        }
                    }
                    catch (Exception ex)
                    {

                        throw;
                    }
                    var getID = empRoot.empType.Where(x => x.EmployeeType == EmployeeType).FirstOrDefault();
                    return getID.ID;
                    
                }

            }
            catch (Exception)
            {
                throw;
            }

            return 0;
        }
        #endregion

        #region ChangePassword

        public async Task<bool> Changepassword(int userID ,string oldPassword, string newPassword, string repeatPassword)
        {
            PasswordModel passwordModel = new PasswordModel()
            {
                NewPassword = newPassword,
                OldPassword = oldPassword,
                RepeatNewPassword = repeatPassword
            };

            try
            {
                using HttpRequestMessage requestMessage = new HttpRequestMessage(HttpMethod.Patch, _url + "password?userID=" + userID);
                requestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));

                requestMessage.Content = JsonContent.Create(passwordModel);
                HttpResponseMessage response = await _client.SendAsync(requestMessage);
                if (response.IsSuccessStatusCode)
                {
                    return true;
                }
            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
                
            }
            return false;
        }

        #endregion
    }
}
