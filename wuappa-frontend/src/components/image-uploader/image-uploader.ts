import { Component, Output, EventEmitter } from '@angular/core';
import { AlertController } from 'ionic-angular';
import { Camera, CameraOptions } from '@ionic-native/camera';
import { UploadService } from '../../providers/upload-service';
import { LoadingController } from 'ionic-angular/components/loading/loading-controller';
import { TranslateService } from '@ngx-translate/core';


@Component({
  selector: 'image-uploader',
  templateUrl: 'image-uploader.html'
})
export class ImageUploaderComponent {

  @Output() onUploadFinished: EventEmitter<any> = new EventEmitter<any>();

  translations = {};

   options: CameraOptions = {
    quality: 100,
    sourceType: this.camera.PictureSourceType.CAMERA,
    destinationType: this.camera.DestinationType.DATA_URL,
    encodingType: this.camera.EncodingType.JPEG,
    mediaType: this.camera.MediaType.PICTURE,
    targetWidth: 512,
    targetHeight: 512,
  };

  constructor(
    private camera: Camera,
    private alertCtrl: AlertController,
    private uploadService: UploadService,
    private loadingCtrl: LoadingController,
    private translate: TranslateService
  ) {
    this.translate.get([
      'Select an option',
      'Select an option for the picture',
      'Camera',
      'Gallery',
      'Loading',
      'OK'
    ]).subscribe(result => this.translations = result);
  }

  selectSource(){
    let source: number;
    this.alertCtrl.create({
      title: this.translations['Select an option'],
      subTitle: this.translations['Select an option for the picture'],
      buttons: [{
        text: this.translations['Camera'],
        role: this.translations['Camera'],
        handler: () => {
          source = this.camera.PictureSourceType.CAMERA;
          this.options.sourceType = source;
          this.getPicture();
        }
      }, {
          text: this.translations['Gallery'],
          role: this.translations['Gallery'],
          handler: () => {
            source = this.camera.PictureSourceType.PHOTOLIBRARY;
            this.options.sourceType = source;
            this.getPicture();
          }
      }]
    }).present();
  }

  getPicture(){
    this.camera.getPicture(this.options).then((imageData) => {
      let base64Image = 'data:image/jpeg;base64,' + imageData;
      this.uploadImage(base64Image);
    }, err => {
      this.alertCtrl.create({ message: err, buttons: [this.translations["OK"]] }).present();
    });
  }

  uploadImage(image) {
    let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    this.uploadService.upload(image).subscribe(data => {
      const response = data as any; // STC: Stupid TypeScript Cast
      this.onUploadFinished.emit(response.file);
      loader.dismiss();
    }, error => {
      loader.dismiss();
      this.alertCtrl.create({ message: this.uploadService.errorToString(error), buttons: [this.translations["OK"]] }).present();
    });
  }

}
