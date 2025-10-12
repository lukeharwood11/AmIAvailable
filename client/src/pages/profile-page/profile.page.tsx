import React, { useState, useEffect, useCallback } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useSearchParams } from 'react-router-dom';
import { RootState, AppDispatch } from '../../redux/store';
import Card from '../../components/card/Card';
import Text from '../../components/text/Text';
import Button from '../../components/button/Button';
import styles from './profile.page.module.css';
import { TabItem, Tabs } from '../../components';
import { fetchUserRelationshipsThunk } from '../../redux/thunks/relationships.thunk';
import {
  fetchReceivedRelationshipRequestsThunk,
  approveRelationshipRequestThunk,
  rejectRelationshipRequestThunk,
  fetchSentRelationshipRequestsThunk,
} from '../../redux/thunks/relationship-requests.thunk';
import { RelationshipWithUserData } from '../../redux/types/relationships.types';
import { RelationshipRequestWithUserData } from '../../redux/types/relationship-requests.types';
import { MdAccountCircle, MdPerson, MdSettings, MdTrendingUp } from 'react-icons/md';
import { useMediaQuery } from 'react-responsive';
import { AiUsageTab } from './components';

const ProfilePage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState('account-information');
  const smallDevice = useMediaQuery({ query: '(max-width: 768px)' });

  const user = useSelector((state: RootState) => state.auth.session?.user);
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );

  // Relationships state
  const relationships = useSelector(
    (state: RootState) => state.relationships.relationships
  );
  const relationshipRequests = useSelector(
    (state: RootState) => state.relationships.relationshipRequests.received
  );
  const sentRelationshipRequests = useSelector(
    (state: RootState) => state.relationships.relationshipRequests.sent
  );
  const relationshipsLoading = useSelector(
    (state: RootState) => state.relationships.loading.relationships
  );
  const relationshipRequestsLoading = useSelector(
    (state: RootState) => state.relationships.loading.relationshipRequests
  );

  // Initialize active tab from URL params
  useEffect(() => {
    const tabFromUrl = searchParams.get('tab');
    if (
      tabFromUrl &&
      ['account-information', 'settings', 'relationships', 'ai-usage'].includes(
        tabFromUrl
      )
    ) {
      setActiveTab(tabFromUrl);
    }
  }, [searchParams]);

  // Update URL when tab changes
  const handleTabChange = useCallback(
    (tabId: string) => {
      setActiveTab(tabId);
      setSearchParams({ tab: tabId });
    },
    [setSearchParams]
  );

  // Load relationships data when relationships tab is active
  useEffect(() => {
    dispatch(fetchUserRelationshipsThunk({}));
    dispatch(fetchReceivedRelationshipRequestsThunk('pending'));
    dispatch(fetchSentRelationshipRequestsThunk('pending'));
  }, [dispatch]);

  const handleApproveRequest = useCallback(
    async (requestId: string) => {
      try {
        await dispatch(
          approveRelationshipRequestThunk(requestId)
        ).unwrap();
        // Refresh the data
        dispatch(fetchReceivedRelationshipRequestsThunk(undefined));
        dispatch(fetchUserRelationshipsThunk({}));
      } catch (error) {
        console.error('Failed to approve relationship request:', error);
      }
    },
    [dispatch]
  );

  const handleRejectRequest = useCallback(
    async (requestId: string) => {
      try {
        await dispatch(
          rejectRelationshipRequestThunk(requestId)
        ).unwrap();
        // Refresh the data
        dispatch(fetchReceivedRelationshipRequestsThunk(undefined));
      } catch (error) {
        console.error('Failed to reject relationship request:', error);
      }
    },
    [dispatch]
  );

  if (!isAuthenticated || !user) {
    return (
      <div className={styles.profilePage}>
        <div className={styles.container}>
          <Card variant='default' padding='large'>
            <Text variant='heading' color='grey-800'>
              Not authenticated
            </Text>
            <Text variant='body' color='grey-600'>
              Please log in to view your profile.
            </Text>
          </Card>
        </div>
      </div>
    );
  }

  const userMetadata = user.user_metadata || {};
  const appMetadata = user.app_metadata || {};

  // Relationships tab content
  const renderRelationshipsContent = () => (
    <div className={styles.relationshipsContent}>
      {/* Active Relationships */}
      <Card
        variant='default'
        padding='large'
        className={styles.relationshipsCard}
      >
        <div className={styles.cardHeader}>
          <Text variant='heading-small' color='grey-800'>
            Your Relationships
          </Text>
        </div>
        {relationshipsLoading ? (
          <Text variant='body' color='grey-600'>
            Loading relationships...
          </Text>
        ) : relationships.length === 0 ? (
          <Text variant='body' color='grey-600'>
            No relationships yet.
          </Text>
        ) : (
          <div className={styles.relationshipsList}>
            {relationships.map(
              (relationship: RelationshipWithUserData) => (
                <div
                  key={relationship.id}
                  className={styles.relationshipItem}
                >
                  <div className={styles.relationshipInfo}>
                    <Text
                      variant='body'
                      color='grey-800'
                      weight='medium'
                    >
                      {relationship.other_user.full_name
                        ? `${relationship.other_user.full_name} (${relationship.other_user.email})`
                        : relationship.other_user.email}
                    </Text>
                    <Text
                      variant='body-small'
                      color='grey-600'
                    >
                      Connected since{' '}
                      {new Date(
                        relationship.created_at
                      ).toLocaleDateString()}
                    </Text>
                  </div>
                </div>
              )
            )}
          </div>
        )}
      </Card>

      {/* Received Relationship Requests */}
      <Card
        variant='default'
        padding='large'
        className={styles.requestsCard}
      >
        <div className={styles.cardHeader}>
          <Text variant='heading-small' color='grey-800'>
            Received Requests
          </Text>
        </div>
        {relationshipRequestsLoading ? (
          <Text variant='body' color='grey-600'>
            Loading requests...
          </Text>
        ) : relationshipRequests.length === 0 ? (
          <Text variant='body' color='grey-600'>
            No pending requests.
          </Text>
        ) : (
          <div className={styles.requestsList}>
            {relationshipRequests.map(
              (request: RelationshipRequestWithUserData) => (
                <div
                  key={request.id}
                  className={styles.requestItem}
                >
                  <div className={styles.requestInfo}>
                    <Text
                      variant='body'
                      color='grey-800'
                      weight='medium'
                    >
                      {request.requester.full_name
                        ? `${request.requester.full_name} (${request.requester.email})`
                        : request.requester.email}
                    </Text>
                    <Text
                      variant='body-small'
                      color='grey-600'
                    >
                      Requested on{' '}
                      {new Date(
                        request.created_at
                      ).toLocaleDateString()}
                    </Text>
                  </div>
                  <div className={styles.requestActions}>
                    <Button
                      variant='primary'
                      size='small'
                      onClick={() =>
                        handleApproveRequest(request.id)
                      }
                      disabled={
                        request.status === 'accepted'
                      }
                    >
                      Accept
                    </Button>
                    <Button
                      variant='secondary'
                      size='small'
                      onClick={() =>
                        handleRejectRequest(request.id)
                      }
                      disabled={
                        request.status === 'rejected'
                      }
                    >
                      Decline
                    </Button>
                  </div>
                </div>
              )
            )}
          </div>
        )}
      </Card>

      {/* Sent Relationship Requests */}
      <Card
        variant='default'
        padding='large'
        className={styles.requestsCard}
      >
        <div className={styles.cardHeader}>
          <Text variant='heading-small' color='grey-800'>
            Pending Requests
          </Text>
        </div>
        {relationshipRequestsLoading ? (
          <Text variant='body' color='grey-600'>
            Loading requests...
          </Text>
        ) : sentRelationshipRequests.length === 0 ? (
          <Text variant='body' color='grey-600'>
            No pending requests.
          </Text>
        ) : (
          <div className={styles.requestsList}>
            {sentRelationshipRequests.map((request: any) => (
              <div
                key={request.id}
                className={styles.requestItem}
              >
                <div className={styles.requestInfo}>
                  <Text
                    variant='body'
                    color='grey-800'
                    weight='medium'
                  >
                    {request.requested_email}
                  </Text>
                  <Text variant='body-small' color='grey-600'>
                    Sent on{' '}
                    {new Date(
                      request.created_at
                    ).toLocaleDateString()}
                  </Text>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );

  // Settings tab content
  const renderSettingsContent = () => (
    <Card variant='default' padding='large'>
      <Text variant='heading-small' color='grey-800'>
        Settings
      </Text>
      <Text variant='body' color='grey-600'>
        In Progress...
      </Text>
    </Card>
  );

  const sampleTabs: TabItem[] = [
    {
      id: 'account-information',
      label: 'Account',
      icon: smallDevice ? undefined : <MdAccountCircle size={20} />,
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: smallDevice ? undefined : <MdSettings size={20} />,
      content: renderSettingsContent(),
    },
    {
      id: 'relationships',
      label: 'Relationships',
      icon: smallDevice ? undefined : <MdPerson size={20} />,
      content: renderRelationshipsContent(),
    },
    {
      id: 'ai-usage',
      label: 'AI Usage',
      icon: smallDevice ? undefined : <MdTrendingUp size={20} />,
      content: <AiUsageTab />,
    },
  ];

  return (
    <div className={styles.profilePage}>
      <div className={styles.container}>
        <div className={styles.header}>
          <Text variant='heading-large' color='grey-800'>
            Profile
          </Text>
          <Text variant='body' color='grey-600'>
            Your account information and settings
          </Text>
        </div>

        <div className={styles.content}>
          <Tabs
            useMobileMenu
            variant='underlined'
            tabs={sampleTabs}
            activeTabId={activeTab}
            onTabChange={handleTabChange}
          />

          {activeTab === 'account-information' && (
            <Card
              variant='default'
              padding='large'
              className={styles.infoCard}
            >
              <div className={styles.cardHeader}>
                <Text variant='heading-small' color='grey-800'>
                  Account Information
                </Text>
              </div>

              <div className={styles.infoGrid}>
                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Name
                  </Text>
                  <Text variant='body' color='grey-800'>
                    {userMetadata.name ||
                      userMetadata.full_name ||
                      'Not provided'}
                  </Text>
                </div>

                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Email
                  </Text>
                  <Text variant='body' color='grey-800'>
                    {user.email || 'Not provided'}
                  </Text>
                </div>

                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Provider
                  </Text>
                  <Text variant='body' color='grey-800'>
                    {appMetadata.provider || 'Unknown'}
                  </Text>
                </div>

                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Email Verified
                  </Text>
                  <Text
                    variant='body'
                    color={
                      user.email_confirmed_at
                        ? 'primary'
                        : 'danger'
                    }
                  >
                    {user.email_confirmed_at ? 'Yes' : 'No'}
                  </Text>
                </div>

                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Account Created
                  </Text>
                  <Text variant='body' color='grey-800'>
                    {user.created_at
                      ? new Date(
                        user.created_at
                      ).toLocaleDateString()
                      : 'Unknown'}
                  </Text>
                </div>

                <div className={styles.infoItem}>
                  <Text
                    variant='body-small'
                    color='grey-600'
                    weight='medium'
                  >
                    Last Sign In
                  </Text>
                  <Text variant='body' color='grey-800'>
                    {user.last_sign_in_at
                      ? new Date(
                        user.last_sign_in_at
                      ).toLocaleDateString()
                      : 'Unknown'}
                  </Text>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
