import { Injectable } from '@angular/core';
import { APIService } from './api-service';

@Injectable()
export class UploadService extends APIService {

  upload(data){
    if (data) {
      return this.http.post(this.getApiUrl('upload'), { file: data });
    } else {
      return null;
    }
  }

}
