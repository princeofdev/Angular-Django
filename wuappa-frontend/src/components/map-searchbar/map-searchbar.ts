import { Component, NgZone, AfterViewInit, ViewChild, Output, EventEmitter, ElementRef, Input, OnChanges } from '@angular/core';
import {} from 'googlemaps';
import { MapsAPILoader } from '@agm/core';


@Component({
  selector: 'map-searchbar',
  templateUrl: 'map-searchbar.html'
})
export class MapSearchbarComponent  implements AfterViewInit, OnChanges {

  @ViewChild('searchInput') searchInput: ElementRef;
  @Input() coords = { lat: null, lng: null };
  @Output() onChange: EventEmitter<any> = new EventEmitter<any>();

  private autocomplete = null;

  constructor(
    private mapsAPILoader: MapsAPILoader,
    private ngZone: NgZone
  ) { }

  ngOnChanges(changes) {
    if (this.autocomplete && changes.coords && this.coords.lat && this.coords.lng) {
      var circle = new google.maps.Circle({
        center: { lat: this.coords.lat, lng: this.coords.lng }, radius: 100
      });
      this.autocomplete.setBounds(circle.getBounds());
    }
  }

  ngAfterViewInit(){
    this.mapsAPILoader.load().then(() => {
      this.autocomplete = new google.maps.places.Autocomplete(this.searchInput.nativeElement, { types: [] });
      this.autocomplete.addListener("place_changed", () => {
        this.ngZone.run(() => {
          //get the place result
          let place: google.maps.places.PlaceResult = this.autocomplete.getPlace();
          let location = {
            address: "",
            address_details: "",
            city: "",
            state: "",
            country: "",
            zip: ""
          };
          let address_components = place['address_components'] || [];
          if (address_components.length == 0) {
            location.address = place.name || "";
          } else {
            for (let component of address_components) {
              if (component.types && component.types.indexOf("street_number") >= 0) {
                location["address_details"] += component.long_name;
              }
              if (component.types && component.types.indexOf("route") >= 0) {
                location["address"] = component.long_name;
              }
              if (component.types && component.types.indexOf("locality") >= 0) {
                location["city"] = component.long_name;
              }
              if (component.types && component.types.indexOf("administrative_area_level_2") >= 0) {
                location["state"] = component.long_name;
              }
              if (component.types && component.types.indexOf("country") >= 0) {
                location["country"] = component.long_name;
              }
              if (component.types && component.types.indexOf("postal_code") >= 0) {
                location["postal_code"] = component.long_name;
              }
            }
          }
          this.onChange.emit(location);
        });
      });
    });
  }
}
