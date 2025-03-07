import {
  AntButton as Button,
  Box,
  LinkIcon,
  TabList,
  Tabs,
  useDisclosure,
} from "fidesui";
import type { NextPage } from "next";
import React from "react";

import { FidesTab } from "~/features/common/DataTabs";
import FidesSpinner from "~/features/common/FidesSpinner";
import Layout from "~/features/common/Layout";
import PageHeader from "~/features/common/PageHeader";
import { useGetAllDatastoreConnectionsQuery } from "~/features/datastore-connections/datastore-connection.slice";
import AddIntegrationModal from "~/features/integrations/add-integration/AddIntegrationModal";
import getIntegrationTypeInfo, {
  SUPPORTED_INTEGRATIONS,
} from "~/features/integrations/add-integration/allIntegrationTypes";
import IntegrationList from "~/features/integrations/IntegrationList";
import useIntegrationFilterTabs from "~/features/integrations/useIntegrationFilterTabs";

const IntegrationListView: NextPage = () => {
  const { data, isLoading } = useGetAllDatastoreConnectionsQuery({
    connection_type: SUPPORTED_INTEGRATIONS,
  });

  const { onOpen, isOpen, onClose } = useDisclosure();
  const {
    tabIndex,
    onChangeFilter,
    anyFiltersApplied,
    isFiltering,
    filteredTypes,
    tabs,
  } = useIntegrationFilterTabs(
    data?.items?.map((i) => getIntegrationTypeInfo(i.connection_type)),
  );

  const integrations =
    data?.items.filter((integration) =>
      filteredTypes.some(
        (type) =>
          type.placeholder.connection_type === integration.connection_type,
      ),
    ) ?? [];

  return (
    <Layout title="Integrations">
      <PageHeader
        heading="Integrations"
        breadcrumbItems={[
          {
            title: "All integrations",
          },
        ]}
      />
      <Box data-testid="integration-tabs" display="flex">
        <Tabs index={tabIndex} onChange={onChangeFilter} w="full">
          <TabList>
            {tabs.map((label) => (
              <FidesTab label={label} key={label} />
            ))}
          </TabList>
        </Tabs>
        <Box
          borderBottom="2px solid"
          borderColor="gray.200"
          height="fit-content"
          pr="2"
          pb="2"
        >
          <Button
            onClick={onOpen}
            data-testid="add-integration-btn"
            icon={<LinkIcon />}
            iconPosition="end"
          >
            Add Integration
          </Button>
        </Box>
      </Box>
      {isLoading || isFiltering ? (
        <FidesSpinner />
      ) : (
        <IntegrationList
          integrations={integrations}
          onOpenAddModal={onOpen}
          isFiltered={anyFiltersApplied}
        />
      )}
      <AddIntegrationModal isOpen={isOpen} onClose={onClose} />
    </Layout>
  );
};

export default IntegrationListView;
