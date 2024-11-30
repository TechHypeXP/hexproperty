import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Property, CreatePropertyDTO, UpdatePropertyDTO, TenantId } from '@/domain/models/property/property';
import { GetPropertiesUseCase } from '@/application/usecases/property/get-properties.usecase';
import { propertyKeys } from '@/interface/queries/queryKeys';

export const useProperties = (tenantId: TenantId) => {
  const queryClient = useQueryClient();
  const getPropertiesUseCase = new GetPropertiesUseCase(/* inject propertyService */);

  const {
    data: properties,
    isLoading,
    error,
  } = useQuery<Property[]>({
    queryKey: propertyKeys.list(tenantId),
    queryFn: () => getPropertiesUseCase.execute(tenantId),
  });

  const createProperty = useMutation({
    mutationFn: (data: CreatePropertyDTO) => {
      // Implement create property
      return Promise.resolve({} as Property);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: propertyKeys.list(tenantId) });
    },
  });

  const updateProperty = useMutation({
    mutationFn: (data: UpdatePropertyDTO) => {
      // Implement update property
      return Promise.resolve({} as Property);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: propertyKeys.list(tenantId) });
    },
  });

  return {
    properties,
    isLoading,
    error,
    createProperty,
    updateProperty,
  };
};
