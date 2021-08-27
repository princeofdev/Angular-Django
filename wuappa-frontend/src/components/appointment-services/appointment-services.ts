import { Component, Input } from '@angular/core';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'appointment-services',
  templateUrl: 'appointment-services.html'
})
export class AppointmentServicesComponent implements OnInit {

  @Input() services: any = [];
  text: string = "";
  
  ngOnInit(){
    let servicesDict = {};
    for (let service of this.services) {
      let serviceItem = servicesDict[service.id] || { name: service.name, count: 0 };
      serviceItem.count++;
      servicesDict[service.id] = serviceItem;
    }
    for (let key of Object.keys(servicesDict)) {
      let service = servicesDict[key];
      this.text += `${service.count}x ${service.name}. `;
    }
  }

}
