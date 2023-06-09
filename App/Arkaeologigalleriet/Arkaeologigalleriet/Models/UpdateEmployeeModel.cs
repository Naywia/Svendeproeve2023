﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{
    public class UpdateEmployeeModel
    {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Email { get; set; }
        public int PhoneNumber { get; set; }
        public string Address { get; set; }
        public int Postal { get; set; }
        public string City { get; set; }
        public int EmployeeTypeID { get; set; }
    }
}
