import { Component, Input } from '@angular/core';

@Component({
  selector: 'profile',
  templateUrl: 'profile.html'
})
export class ProfileComponent {

  @Input()
  user: any;

  constructor() {}

  getPicture() {
    if (this.user.profile && this.user.profile.picture) {
      return this.user.profile.picture;
    }
    return '/assets/imgs/profile-default-image.png';
  }

}
