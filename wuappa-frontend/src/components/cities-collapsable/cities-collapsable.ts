import { Component, Input, OnChanges, Output, EventEmitter } from '@angular/core';
import { log } from 'util';
import { SelectorMatcher } from '@angular/compiler';
import { OutputEmitter } from '@angular/compiler/src/output/abstract_emitter';

/**
 * Generated class for the CitiesCollapsableComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'cities-collapsable',
  templateUrl: 'cities-collapsable.html'
})
export class CitiesCollapsableComponent {

  @Input() zones:any = [];
  @Input() citySelected:any = [];
  @Input() zonesAdded:any = [];
  @Output() collectZone: EventEmitter<any> = new EventEmitter<any>();
  @Output() removeZone: EventEmitter<any> = new EventEmitter<any>();
  private zoneList:any = [];
  public itemActive:any = null;
  public indexActive:any = null;
  public zonesSelected:any = [];
  constructor() {
    
  }
  
  ngOnChanges(){
    this.selectCityIdFromWorkZone();
    
    console.log("micity", this.citySelected);
  }

  selectCityIdFromWorkZone(){
    this.zoneList = []
    for (let i in this.zones){
      let zones = this.zones[i]
      for(let zone in zones){
        this.zoneList.push(zones[zone]);
      }
    }
  }

  displayCorrectArrow(index){
   return this.indexActive == index;
  }

  setItemActive(cityId, index){
    this.itemActive = cityId
    this.indexActive = index
  }

  showZonesByCity(zoneId, index){
    return this.itemActive === zoneId && this.indexActive === index
  }

  addZone(zone){
    this.collectZone.emit(zone)
  }

  deleteZone(zone){
    this.removeZone.emit(zone)
  }

  zoneIsSelected(zone){
    return this.zonesAdded.indexOf(zone) != -1;
  }
  

}