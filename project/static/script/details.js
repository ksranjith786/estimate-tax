$(document).ready(function () {
    $('#details_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            first_name: {
                validators: {
                    stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please supply your first name'
                    }
                }
            },
            last_name: {
                validators: {
                    stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please supply your last name'
                    }
                }
            },/*
            email: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your email address'
                    },
                    emailAddress: {
                        message: 'Please supply a valid email address'
                    }
                }
            },
            phone: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your phone number'
                    },
                    phone: {
                        country: 'US',
                        message: 'Please supply a valid phone number with area code'
                    }
                }
            },
            city: {
                validators: {
                    stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please supply your city'
                    }
                }
            },
            age: {
                validators: {
                    notEmpty: {
                        message: 'Age is required'
                    },
                    numeric: {
                        message: 'The value is not a valid number'
                    },
                    lessThan: {
                        value: 18,
                        message: 'Please enter a value more than or equal to 18'
                    },
                    greaterThan: {
                        value: 100,
                        message: 'Please enter a value less than or equal to 100'
                    },
                }
            },*/
            basic_pay: {
                validators: {
                    notEmpty: {
                        message: 'Basic Pay is required'
                    },
                    numeric: {
                        message: 'The value is not a valid number'
                    },
                    lessThan: {
                        value: 1000,
                        message: 'Please enter a value more than or equal to 1000'
                    },
                    greaterThan: {
                        value: 1000000000,
                        message: 'Please enter a value less than or equal to 1000000000'
                    }
                }
            }
        }
    })
    .on('success.form.bv', function (e) {
        $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
        $('#contact_form').data('bootstrapValidator').resetForm();

        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        $.post($form.attr('action'), $form.serialize(), function (result) {
            console.log(result);
        }, 'json');
    });
});
