angular.module("BongApp.Subscriptions", [
    "BongApp.Common",
]).controller('SubscriptionsController', function($rootScope, $scope, $state, $http){
    if ((typeof $rootScope.bongAuthToken !== 'string') || ($rootScope.bongAuthToken.length === 0)) {
        $state.go('login');
        return;
    }
    $scope.predicate = '-total_subscriptions';
    $http.defaults.headers.common["X-Bong-Token"] = $rootScope.bongAuthToken;
    $http.get($rootScope.BASE_URL + '/api/deal').success(function(data, status, headers, config) {
        var current_deals = [];
        var pending_deals = [];
        angular.forEach(data, function(value){
            if (value.total_subscriptions < 1) {
                return;
            }

            if (value.status === 4) {
                pending_deals.push(value);
            } else if (value.status === 2) {
                current_deals.push(value);
            }

        });

        $scope.pending_deals = pending_deals;
        $scope.current_deals = current_deals;
    });

    $scope.ShowUsers = function(deal){
        $scope.selectedDeal = deal;
        $http.get($rootScope.BASE_URL + '/api/deal/'+deal.id+'/subscriptions').success(function(data, status, headers, config) {
            $scope.subscriptions = data.data;
        });
        return false;
    };
});
