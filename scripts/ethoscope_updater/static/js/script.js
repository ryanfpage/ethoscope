(function(){
    var app = angular.module('updater', ['ngRoute']);
    app.filter("toArray", function(){
        return function(obj) {
            var result = [];
            angular.forEach(obj, function(val, key) {
                result.push(val);
            });
            return result;
        };
    });

    // create the controller and inject Angular's $scope
    app.controller('mainController', function($scope, $window, $http, $interval, $timeout) {
        $scope.system = {};
        $scope.system.isUpdated = false;
        $scope.node ={};
        $scope.devices={};
        $scope.groupActions={};
        $scope.branch_to_switch= null;
        $scope.system.modal_error = "";
        $scope.spinner= new Spinner(opts).spin();
        var loadingContainer = document.getElementById('loading_devices');
        loadingContainer.appendChild($scope.spinner.el);
        $scope.spinner_text = 'Fetching, please wait...';

        $scope.spinner_scan= new Spinner(opts).spin();
        var loadingContainer_scan = document.getElementById('scanning_devices');
        loadingContainer_scan.appendChild($scope.spinner_scan.el);


        $http.get('/bare/update').success(function(data){
            console.log(data);
            if ('error' in data){
                $scope.system.error= data.error;
                console.log($scope.system.isUpdated);
            }else{
                $scope.system.isUpdated = true;
                $scope.system.status = data;
                console.log($scope.system.isUpdated);
            }
            $scope.spinner.stop();
            $scope.spinner = false;
            $scope.spinner_text = null;

        });
        $http.get('/devices').success(function(data){
            check_error(data);
            $scope.devices = data;

            //slower method is the one that has to stop the spinner
            $scope.spinner_scan.stop();
            $scope.spinner_scan = false;

            console.log($scope.devices);
        });
        $http.get('/device/check_update/node').success(function(data){
           check_error(data);
            $scope.node.check_update = data;
        });
        $http.get('/device/active_branch/node').success(function(data){
            check_error(data);
            $scope.node.active_branch = data.active_branch;
        });
        //aADD A call to node/info
        $http.get('/node_info').success(function(data){
            check_error(data);
            $scope.node.ip = data.ip;
            $scope.node.status = data.status;
            $scope.node.id= data.id;
        });
        
        //Update
        $scope.devices_to_update_selected = [];
        
        $scope.pre_update = function(devices_to_update){
           spin("start");
           error = check_devices_state(devices_to_update, "running");
           $("#updateModal").modal('show');
            spin("stop");

        };
        $scope.update = function(devices_to_update){
            //close modal
             $("#updateModal").modal('hide');
            //start spin
            spin("start");
            data = {"devices":devices_to_update}
            $http.post('/group/update', data = data)
                 .success(function(data){
                    check_error(data);
                    $scope.update_result= data;
                    spin("stop");
                    $window.location.reload();

            })
        };
        
        
        $scope.pre_restart = function(devices_to_restart){
             spin("start");
            error = check_devices_state(devices_to_restart, "running");

            //open modal
            $("#restartModal").modal('show');
            //stop spin
            spin("stop");


        }
        $scope.restart = function(devices_to_restart){
            //close modal
             $("#restartModal").modal('hide');
            //start spin
            spin("start");
            
            data = {"devices":devices_to_restart}
            $http.post('/group/restart', data = data)
                 .success(function(data){
                    check_error(data);
                    $scope.update_result= data;
                    spin("stop");
                    $window.location.reload();

            })
        }
        
        $scope.pre_swBranch = function(devices_to_switch){
            spin("start");
            error = check_devices_state(devices_to_switch, "running");

            //open modal
            $("#swBranchModal").modal('show');
            //stop spin
            spin("stop");

        };
        
        $scope.swBranch = function(devices_to_switch){
            //close modal
             $("#swBranchModal").modal('hide');
            //start spin
            spin("start");
            for (device in devices_to_switch){
                devices_to_switch[device]['new_branch'] = $scope.branch_to_switch;
            }
            data = {"devices":devices_to_switch}
            $http.post('/group/swBranch', data = data)
                 .success(function(data){
                    check_error(data);
                    $scope.update_result= data;
                    spin("stop");
                    $window.location.reload();

            })
        }
        //HELPERS
        $scope.secToDate = function(secs){
            d = new Date(secs*1000);
            return d.toString();
        };
        
        spin = function(action){
        if (action=="start"){
             $scope.spinner= new Spinner(opts).spin();
            var loadingContainer = document.getElementById('loading_devices');
            loadingContainer.appendChild($scope.spinner.el);
        }else if (action=="stop"){
             $scope.spinner.stop();
             $scope.spinner = false;
        }
        };
        
        check_devices_state = function(devices, state){
            var error = false;
                $scope.system.modal_error = "";
                if(devices.length == 0){
                    $scope.system.modal_error = "No device selected. Please tick some boxes!";
                    return true;
                }

                for (device in devices){
                    if (device.status == state){
                        $scope.system.error="One or more selected devices are "+state+" and cannot be updated, check selection"
                        return true;

                    }
                };
                return false;
        };
        
        check_error = function(data){
            if ('error' in data){
                $scope.system.error= data.error;
            }
        };
        

        $scope.groupActions.checkStart = function(selected_devices){
            softwareVersion = "";
            device_version = "";
            checkVersionLoop:
            for (var i = 0; i< selected_devices.length(); i++){
                    $http.get('/device/'+selected_devices[i]+'/data').success(function(data){device_version = data.version.id});
                    if (i == 0) {
                        softwareVersion = device_version;
                    }
                    if (softwareVersion != device_version){
                        break checkVersionLoop;
                    }
            }
        };

        $scope.groupActions.start = function(){
                            $("#startModal").modal('hide');
                            spStart= new Spinner(opts).spin();
                            starting_tracking.appendChild(spStart.el);
                            $http.post('/device/'+device_id+'/controls/start', data=option)
                                 .success(function(data){$scope.device.status = data.status;});
             $http.get('/devices').success(function(data){
                    $http.get('/device/'+device_id+'/data').success(function(data){
                        $scope.device = data;

                    });

                    $http.get('/device/'+device_id+'/ip').success(function(data){
                        $scope.device.ip = data;
                        device_ip = data;
                    });
                 $("#startModal").modal('hide');
            });
        };



    });

}
)()
