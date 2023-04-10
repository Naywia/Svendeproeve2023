using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{
    public class ArtifactInformationModel : INotifyPropertyChanged
    {
        private int _ID;

        public int ID
        {
            get { return _ID; }
            set { _ID = value; }
        }

        private string _Name;

        public string Name
        {
            get { return _Name; }
            set { _Name = value; }
        }

        private string _Description;

        public string Description
        {
            get { return _Description; }
            set { _Description = value; }
        }
        private string _ArtefactType;

        public string ArtefactType
        {
            get { return _ArtefactType; }
            set { _ArtefactType = value; }
        }
        private string _Storage;

        public string Storage
        {
            get { return _Storage; }
            set { _Storage = value; }
        }

        private int _Shelf;

        public int Shelf
        {
            get { return _Shelf; }
            set { _Shelf = value; }
        }

        private string _Row;

        public string Row
        {
            get { return _Row; }
            set { _Row = value; }
        }


        public event PropertyChangedEventHandler PropertyChanged;

        private void NotifyPropertyChanged([CallerMemberName] String propertyName = "")
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
}
