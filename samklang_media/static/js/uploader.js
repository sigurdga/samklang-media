/*
---

name: Uploader

description: File uploader with HTML5 support and IFrame fallback

version: 0.1a

license: MIT

authors:
 - Jørgen Bergquist

...
*/

Uploader = new Class ({
    Implements: [Options, Events],

    options: {
        dropText: 'Drop your files here',
        rowselector: '.ctrlHolder',
        autoupload: true
    },

    initialize: function(input, options) {
        this.setOptions(options);
        this.input = document.id(input);
        this.form = this.input.getParent("form");
        if (!this.form) return;

        // sniffing
        this.isHTML5 = 'multiple' in new Element('input[type=file]')
            && typeof File != "undefined"
            && typeof FileList != "undefined"
            && typeof FormData != "undefined";

        if (this.isHTML5)
            this.html5uploader();
        else
            this.uploader();
    },

    html5uploader: function() {
        var self = this,
            drop = new Element('div.dropbox').inject(this.input.getPrevious("label"), 'before'),
            message = new Element('span.uploadmessage', {
                text: this.options.dropText
            }).inject(drop, 'top'),
            list = new Element('ul.uploads').inject(drop, 'bottom'),

        	progress = new Element('div.progress').setStyle('display', 'none').inject(list, 'after'),

        	input_files = new Form.MultipleFileInput(this.input, list, drop, {
        		onDragenter: drop.addClass.pass('hover', drop),
        		onDragleave: drop.removeClass.pass('hover', drop),
        		onDrop: function(event) {
                    drop.removeClass.pass('hover', drop);

                    if (this.options.autoupload) {
                        submit_files();
                    }
                }.bind(this)
        	}),

        	upload_request = new Request.File({
        		url: this.form.get('action') || "",
        		onRequest: progress.setStyles.pass({display: 'block', width: 0}, progress),
        		onProgress: function(event){
        		    var loaded = event.loaded, total = event.total;
        		    progress.setStyle('width', parseInt(loaded / total * 100, 10).limit(0, 100) + '%');
        		},
        		onComplete: function(){
        			progress.setStyle('width', '100%');
        			self.fireEvent('complete', arguments);
        			this.reset();
        		}
        	}),

        	inputname = this.input.get('name'),
        	csrftoken = this.form.getElement('input[name="csrfmiddlewaretoken"]');

        this.form.addEvent('submit', function(event){
        	event.preventDefault();
            submit_files();
        }.bind(this));

        var submit_files = function() {
             input_files.getFiles().each(function(file){
        		upload_request.append(inputname , file);
        	});
        	upload_request.append('csrfmiddlewaretoken', csrftoken.get('value'));
        	upload_request.send();
        };
    },

    uploader: function() {
        var parent = this.input.getParent(this.options.rowselector);
        var parent_clone = parent.clone(true, true),
            add = function(event){
                event.preventDefault();
                var new_row = parent_clone.clone(true, true),
                    new_id = String.uniqueID(),
                    new_label = new_row.getElement('label');

                new_row.getElement('input').set('id', new_id).grab(new Element('a.killrow', {
                    text: 'x',
                    events: {
                        click: function(event){
                            event.preventDefault();
                            new_row.destroy();
                        }
                    }
                }), 'after');

                if (new_label) new_label.set('for', new_id);

                new_row.inject(parent, 'after');
            };

        new Element('a.addrow', {
            text: '+',
            events: { click: add }
        }).inject(this.input, 'after');

        this.form.IFrameFormRequest({
            onRequest: function(){
                document.id('upl_status').set('text','start');
            },
            onComplete: function(response){
                this.form.reset();

                // remove all extra input forms
                this.form.getElements('a.killrow').each(function(row){
                    row.fireEvent('click', new Event());
                });
                document.id('upl_status').set('html', response);
            }.bind(this)
        });
    }
});
