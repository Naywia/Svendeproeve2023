using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{
    public class EmpRoot
    {
        public List<EmpTypeModel> empType { get; set; }
    }
    public class EmpTypeModel
    {
        public int ID { get; set; }
        public string EmployeeType { get; set; }
    }   
}
