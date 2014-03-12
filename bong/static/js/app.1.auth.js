angular.module("BongApp.Auth", [
    "BongApp.Common",
]).controller('AuthController', function($rootScope, $scope, $state, $http, localStorageService){
    if ((typeof $rootScope.bongAuthToken === 'string') && ($rootScope.bongAuthToken.length > 0)) {
        $rootScope.bongAuthToken = localStorageService.get("token");
        $state.go('subscriptions');
        return;
    }



    $scope.authenticate = function(){
        $scope.errors = null;
        $http.post($rootScope.BASE_URL + '/api/auth', $scope.login).success(function(data, status, headers, config) {
            var user = data.data;
            if (user.roles.indexOf('admin') < 0) {
                $scope.errors = {"role": "Permission Denied"};
                return
            }
            $rootScope.bongAuthToken = data.data.token;
            localStorageService.add("token", data.data.token);
            $rootScope.user = user;
            $http.defaults.headers.common["X-Bong-Token"] = $rootScope.bongAuthToken;

            var url = [$rootScope.BASE_URL, '/api/user/', user.id, '/accreditation'].join('');
            $http.get(url).success(function(data, status, headers, config) {
                $rootScope.personalInfo = data;
                $state.go('subscriptions');
            });
        }).error(function(data){
            console.log(data)
            if (data.errors) {
                $scope.errors = data.errors;
            }

        });
    };
});
