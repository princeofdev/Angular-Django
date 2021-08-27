import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { URLS } from '../app/api_urls';

@Injectable()
export class APIService {

    constructor(protected http: HttpClient){ }

    public getApiUrl(path, params = null): string {
        let url = URLS[path];
        if (params) {
            url += this.toQueryParams(params);
        }
        return url;
    }

    protected toQueryParams(dict) : string {
        let result = "";
        for (var key in dict) {
            let value = dict[key];
            result += (result != "") ? "&" : "?";
            result += key;
            result += "=";
            result += encodeURI(value);
        }
        return result;
    }

    public errorToString(errors: any, separator: string = " ") {
      if (errors) {
        let errorMessages = [];
        for (let key in errors) {
            const item = errors[key];
            if (Array.isArray(item)) {
                errorMessages = item.concat(errorMessages);
            } else if (typeof item == 	"object") {
                errorMessages.push(this.errorToString(item));
            } else {
                errorMessages.push(item);
            }
        }
        return errorMessages.join(separator);
      } else {
        return "Unknown error";
      }
    }

}
