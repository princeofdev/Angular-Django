import { Component } from '@angular/core';
import { IonicPage, NavController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { TranslateService } from '@ngx-translate/core';
import { ServicesPage } from '../services-page/services-page';

@IonicPage()
@Component({
    selector: 'page-documentation-page',
    templateUrl: 'documentation-page.html',
})
export class DocumentationPage extends UIComponent {

    public documents = [];
    public activeItem = 'FIN';
    public title: any;
    public registerMode: any;
    constructor(
        private navCtrl: NavController,
        private signupService: SignupService,
        private translate: TranslateService,
    ) {
      super();
      this.registerMode = true;
      this.activeItem = this.signupService.getUserType();
      this.getDocuments();
    }
    getDocuments(){
      if(this.activeItem == 'PRO') {
        this.translate.get(["VATNUMBER", "BIN"]).subscribe(
          translations => {
            this.title = translations['DOCUMENTATION'];
            this.documents = [];
            for (let key in translations) {
              const translation = translations[key];
              this.documents.push({ title: translation, url: null });
            }
          }
        );
      } else {
        this.translate.get(["IDPASSPORT", "AVS", "CERTIFICATE"]).subscribe(
          translations => {
            this.documents = [];
            for (let key in translations) {
              const translation = translations[key];
              this.documents.push({ title: translation, url: null });
            }
          }
        );
      }
    }

    imageUploaded(image, document) {
      document.url = image;
    }

    deleteDocument(document) {
      document.url = null;
    }

    allDocumentsReady() {
      return this.documents.filter(item => item.url).length == this.documents.length;
    }

    getDocumentsUrls() {
      return this.documents.map(item => item.url);
    }

    register() {
      this.signupService.setDocuments(this.getDocumentsUrls());
      this.navCtrl.push(ServicesPage,{
        register_mode: true
      });
    }
}
